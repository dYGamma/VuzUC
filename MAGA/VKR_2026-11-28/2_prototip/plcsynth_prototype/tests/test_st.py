"""Тесты подмножества ST: разбор, семантическая проверка, исполнение."""
import pytest

from plcsynth.st import STCompileError, STProgram, STSyntaxError, compile_check, parse
from plcsynth.st.lexer import parse_time_ms, tokenize


def errors(src):
    return [d for d in compile_check(src) if d.level == "error"]


def prog(body, decls="", cycle=10):
    return STProgram(f"PROGRAM main VAR {decls} END_VAR {body} END_PROGRAM "
                     f"CONFIGURATION C RESOURCE R ON PLC TASK T(INTERVAL := T#{cycle}ms, PRIORITY := 0);"
                     f" PROGRAM I WITH T : main; END_RESOURCE END_CONFIGURATION")


def test_time_literals():
    assert parse_time_ms("2s") == 2000
    assert parse_time_ms("1m30s") == 90000
    assert parse_time_ms("1h2m3s4ms") == 3723004
    assert parse_time_ms("1.5s") == 1500
    kinds = [t.kind for t in tokenize("T#250ms TIME#1s INT#-5 REAL#2 16#FF %IX0.1 %QW3")]
    assert kinds == ["TIME", "TIME", "INT", "REAL", "INT", "LOC", "LOC", "EOF"]


def test_comments_and_case_insensitivity():
    p = prog("(* comment *) x := X + 1; // line comment\n", "x : int;")
    p.scan()
    p.scan()
    assert p.get("x") == 2


def test_syntax_error_has_position():
    with pytest.raises(STSyntaxError) as ex:
        parse("PROGRAM main VAR x : INT; END_VAR x := ; END_PROGRAM")
    assert ex.value.line == 1


def test_type_errors_detected():
    msgs = [d.message for d in errors("PROGRAM main VAR i : INT; r : REAL; b : BOOL; END_VAR "
                                      "i := r; r := 1; b := i; IF i THEN END_IF; y := 0; END_PROGRAM")]
    assert len(msgs) == 5
    assert any("необъявлен" in m for m in msgs)


def test_located_type_must_match_size():
    assert errors("PROGRAM main VAR a AT %IX0.0 : INT; END_VAR END_PROGRAM")
    assert not errors("PROGRAM main VAR a AT %IW0 : INT; b AT %QX0.1 : BOOL; END_VAR END_PROGRAM")


def test_int_arithmetic_and_wrap():
    p = prog("a := 7 / 2; b := -7 / 2; c := -7 MOD 2; d := 32767; d := d + 1; e := REAL_TO_INT(2.5);"
             " f := REAL_TO_INT(-2.5);", "a, b, c, d, e, f : INT;")
    p.scan()
    assert (p.get("a"), p.get("b"), p.get("c"), p.get("d"), p.get("e"), p.get("f")) == (3, -3, -1, -32768, 3, -3)


def test_case_and_limit():
    p = prog("CASE s OF 0: r := 1; 1..3, 5: r := 2; ELSE r := 3; END_CASE; x := LIMIT(0.0, y, 10.0);",
             "s, r : INT; x : REAL; y : REAL := 25.0;")
    for s, expect in ((0, 1), (2, 2), (5, 2), (4, 3)):
        p.set("s", s)
        p.scan()
        assert p.get("r") == expect
    assert p.get("x") == 10.0


def test_ton_timing():
    p = prog("t(IN := go, PT := T#100ms); q := t.Q;", "t : TON; go, q : BOOL;")
    p.set("go", True)
    seen = None
    for k in range(30):
        p.rt.now_ms = k * 10
        p.scan()
        if p.get("q") and seen is None:
            seen = k * 10
    assert seen == 100
    p.set("go", False)
    p.scan()
    assert p.get("q") is False


def test_r_trig():
    p = prog("r(CLK := x); n := n + BOOL_TO_INT(r.Q);", "r : R_TRIG; x : BOOL; n : INT;")
    for v in (False, True, True, False, True):
        p.set("x", v)
        p.scan()
    assert p.get("n") == 2


def test_compile_error_raised():
    with pytest.raises(STCompileError):
        STProgram("PROGRAM main VAR x : INT; END_VAR x := TRUE; END_PROGRAM")
