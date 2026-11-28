"""Тесты конвейера синтеза: правила, распознавание, генерация, повторный синтез, REST."""
import copy
import json
import threading
import urllib.request
from pathlib import Path

import pytest
from lxml import etree

from plcsynth.st import STProgram
from plcsynth.synth import synthesize

ROOT = Path(__file__).resolve().parents[1]
SCHEMES = ROOT / "schemes"


def load(name):
    return json.loads((SCHEMES / name).read_text(encoding="utf-8"))


def codes(res):
    return {d.code for d in res.diagnostics}


@pytest.mark.parametrize("path", sorted(SCHEMES.glob("*.json")), ids=lambda p: p.stem)
def test_all_schemes_compile_and_lose_nothing(path):
    r = synthesize(path)
    assert r.ok
    assert r.report["stats"]["channels_lost"] == []
    STProgram(r.st_code)                      # исполнимо интерпретатором
    etree.fromstring(r.plcopen_xml.encode())  # корректный XML


def test_terminals_are_contracted():
    r = synthesize(SCHEMES / "01_motor_direct.json")
    assert r.report["stats"]["terminals_contracted"] == 3
    assert r.report["instances"][0]["variant"] == "с промежуточным реле"


def test_nc_contact_inverts_input():
    r = synthesize(SCHEMES / "01_motor_direct.json")
    assert "Overload := NOT M1_I_Ovl" in r.st_code
    assert "RunFb := M1_I_RunFb" in r.st_code


def test_fatal_unknown_reference():
    s = load("01_motor_direct.json")
    s["connections"].append({"from": "KM1", "to": "DI9.0", "type": "feedback"})
    r = synthesize(s)
    assert not r.ok and r.st_code is None and "S3" in codes(r)


def test_r1_analog_sensor_on_discrete_input():
    s = load("05_tank_level.json")
    for c in s["connections"]:
        if c["from"] == "LT1":
            c["to"] = "DI1.5"
    r = synthesize(s)
    assert "R1" in codes(r)
    assert all(i["name"] != "LT1" for i in r.report["instances"])
    assert r.report["stats"]["channels_lost"] == []


def test_r1_signal_mismatch():
    s = load("05_tank_level.json")
    s["devices"][0]["signal"] = "0-10V"
    assert "R1" in codes(synthesize(s))


def test_r2_two_devices_on_one_channel():
    s = load("06_conveyor.json")
    s["connections"].append({"from": "BG2", "to": "DI1.2", "type": "wire"})
    s["connections"] = [c for c in s["connections"] if not (c["from"] == "BG2" and c["to"] == "DI1.3")]
    assert "R2" in codes(synthesize(s))


def test_r3_overlapping_addresses():
    s = load("01_motor_direct.json")
    s["modules"].append({"id": "DI2", "kind": "DI", "channels": 8, "base": 0})
    s["devices"].append({"id": "SB1", "class": "PushButton", "tag": "SB1"})
    s["connections"].append({"from": "SB1", "to": "DI2.0", "type": "wire"})
    assert "R3" in codes(synthesize(s))


def test_r4_device_not_connected():
    s = load("01_motor_direct.json")
    s["devices"].append({"id": "HL1", "class": "Lamp", "tag": "HL1"})
    assert "R4" in codes(synthesize(s))


def test_r5_missing_required_attribute():
    s = load("05_tank_level.json")
    del s["devices"][0]["range_hi"]
    r = synthesize(s)
    assert "R5" in codes(r)
    assert any(u["reason"].startswith("R5") for u in r.report["unrecognized"])


def test_regeneration_keeps_user_logic():
    logic = (ROOT / "experiments/user_logic/pump_station.st").read_text(encoding="utf-8")
    first = synthesize(SCHEMES / "02_pump_station.json", user_logic=logic)
    s = load("02_pump_station.json")
    s["devices"].append({"id": "PT9", "class": "AnalogSensor", "tag": "PT9", "range_lo": 0.0, "range_hi": 6.0})
    s["connections"].append({"from": "PT9", "to": "AI1.1", "type": "wire"})
    second = synthesize(s, previous_code=first.st_code)
    assert second.ok
    assert "BackupRun(IN := LT1.Fault AND LSH1.Q, PT := T#120s);" in second.st_code
    assert "PT9(" in second.st_code


def test_deterministic_output():
    a = synthesize(SCHEMES / "02_pump_station.json", plcopen=False).st_code
    b = synthesize(SCHEMES / "02_pump_station.json", plcopen=False).st_code
    assert a == b


def test_rest_api():
    from plcsynth.api import make_server
    srv = make_server("127.0.0.1", 0)
    th = threading.Thread(target=srv.serve_forever, daemon=True)
    th.start()
    try:
        port = srv.server_address[1]
        body = json.dumps({"scheme": load("03_valve.json")}).encode()
        req = urllib.request.Request(f"http://127.0.0.1:{port}/api/v1/synthesize", data=body,
                                     headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
        assert data["ok"] and "XV1(" in data["st"] and data["plcopen"].startswith("<?xml")
        bad = copy.deepcopy(load("03_valve.json"))
        bad["modules"] = "oops"
        req = urllib.request.Request(f"http://127.0.0.1:{port}/api/v1/synthesize",
                                     data=json.dumps({"scheme": bad}).encode(), method="POST")
        with pytest.raises(urllib.error.HTTPError) as ex:
            urllib.request.urlopen(req)
        assert ex.value.code == 422
    finally:
        srv.shutdown()
        srv.server_close()
