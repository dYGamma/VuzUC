"""Тесты второго этапа: расширение библиотеки, исправление FB_Valve, новые ФБ в замкнутом контуре."""
import hashlib
import json
from pathlib import Path

from plcsynth.patterns_ext import EXTENDED_LIBRARY
from plcsynth.sim import ReversingStarter, Simulation, StarDeltaStarter, ValveActuator
from plcsynth.st import STProgram
from plcsynth.synth import synthesize

ROOT = Path(__file__).resolve().parents[1]
SCHEMES = ROOT / "schemes"


def test_extension_covers_schemes_7_8_without_core_changes():
    before = {}
    for line in (ROOT / "results" / "core_hashes_before_extension.txt").read_text().splitlines():
        h, p = line.split()
        before[p.split("/")[-1]] = h
    for name, h in before.items():
        assert hashlib.sha256((ROOT / "plcsynth" / name).read_bytes()).hexdigest() == h, name
    for f in ("07_reversing_motor.json", "08_star_delta.json"):
        r = synthesize(SCHEMES / f, library=EXTENDED_LIBRARY)
        assert r.ok and r.report["stats"]["channel_coverage"] == 1.0


def test_extension_does_not_change_base_results():
    for path in sorted(SCHEMES.glob("*.json")):
        rb, re_ = synthesize(path, plcopen=False), synthesize(path, plcopen=False, library=EXTENDED_LIBRARY)
        base = {(i["name"], i["fb"], json.dumps(i["io"], sort_keys=True)) for i in rb.report["instances"]}
        ext = {(i["name"], i["fb"], json.dumps(i["io"], sort_keys=True)) for i in re_.report["instances"]}
        assert base <= ext, path.name


def _run_valve(reverse_at):
    r = synthesize(SCHEMES / "03_valve.json", plcopen=False)
    sim = Simulation(STProgram(r.st_code), [ValveActuator("XV1", "%QX0.0", "%IX0.0", "%IX0.1", travel_s=5.0)])
    sim.probe_var("XV1.Alarm", "Alarm")
    sim.set_var(0.5, "XV1_Open", True).set_var(reverse_at, "XV1_Open", False)
    return sim.run(14.0)


def test_valve_reverse_during_travel_gives_no_false_alarm():
    assert not any(row["Alarm"] for row in _run_valve(5.0))


def test_reversing_interlock():
    r = synthesize(SCHEMES / "07_reversing_motor.json", plcopen=False, library=EXTENDED_LIBRARY)
    st = ReversingStarter("M1", "%QX0.0", "%QX0.1", "%IX0.0", "%IX0.1", "%IX0.2")
    sim = Simulation(STProgram(r.st_code), [st])
    sim.probe("f", lambda s: s.prog.read("%QX0.0")).probe("r", lambda s: s.prog.read("%QX0.1"))
    sim.pulse(0.5, "M1_Fwd").pulse(2.0, "M1_Rev").pulse(2.05, "M1_Fwd").pulse(2.1, "M1_Rev")
    log = sim.run(5.0)
    assert not any(row["f"] and row["r"] for row in log)
    assert st.both_closed_cycles == 0


def test_star_delta_no_overlap():
    r = synthesize(SCHEMES / "08_star_delta.json", plcopen=False, library=EXTENDED_LIBRARY)
    st = StarDeltaStarter("M1", ("%QX0.0", "%QX0.1", "%QX0.2"), ("%IX0.0", "%IX0.1", "%IX0.2"), "%IX0.3")
    sim = Simulation(STProgram(r.st_code), [st])
    sim.probe_var("M1.Running", "Running")
    sim.pulse(0.5, "M1_Start")
    log = sim.run(7.0)
    assert log[-1]["Running"] and st.star_delta_overlap_cycles == 0


def test_identifier_equal_to_std_fb_name_is_rejected():
    from plcsynth.st.interp import compile_check
    src = ("FUNCTION_BLOCK FB_X\nVAR_INPUT x : BOOL; END_VAR\nVAR tOn : TON; END_VAR\n"
           "  tOn(IN := x, PT := T#10ms);\nEND_FUNCTION_BLOCK\n")
    assert any(d.level == "error" and "регистр" in d.message for d in compile_check(src))
