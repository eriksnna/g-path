import pytest

from core.dialect import Dialect, get_dialect
from core.parser import WARNING, parse_gcode
from core.stats import compute_stats
from core.toolpath import Toolpath

ARC_SECONDS = Dialect("teste", dwell_unit=1.0,
                      process_on=frozenset({8}), process_off=frozenset({9}))
ARC_MILLISECONDS = Dialect("teste ms", dwell_unit=0.001,
                           process_on=frozenset({8}), process_off=frozenset({9}))


def test_g04_is_a_timed_event_without_moving():
    result = parse_gcode("G1 X10 F600\nG04 P5", dialect=ARC_SECONDS)
    dwell = result.moves[-1]
    assert dwell.dwell == pytest.approx(5.0)
    assert dwell.start == dwell.end
    assert result.commands["G4"] == 1


def test_dwell_unit_follows_dialect():
    result = parse_gcode("G04 P5000", dialect=ARC_MILLISECONDS)
    assert result.moves[0].dwell == pytest.approx(5.0)


def test_process_flag_follows_dialect_m_codes():
    text = "G1 X1 F100\nM8\nG1 X2 F100\nM9\nG1 X3 F100"
    moves = parse_gcode(text, dialect=ARC_SECONDS).moves
    assert [m.active for m in moves] == [False, True, False]


def test_m_codes_outside_dialect_are_ignored():
    moves = parse_gcode("M8\nG1 X1 F100", dialect=get_dialect("generico")).moves
    assert moves[0].active is False


def test_rapid_flag_marks_g0_moves():
    moves = parse_gcode("G0 X10\nG1 X20 F100", dialect=get_dialect("generico")).moves
    assert [m.rapid for m in moves] == [True, False]


def test_g04_with_zero_or_missing_p_is_ignored():
    assert parse_gcode("G04 P0").moves == []
    assert parse_gcode("G04").moves == []

def test_dwell_time_is_separated_from_rapid_and_cut():
    result = parse_gcode("G1 X10 F600\nG04 P4", dialect=ARC_SECONDS)
    stats = compute_stats(Toolpath(result.moves), result.commands)
    assert stats.dwell_time == pytest.approx(4.0)
    assert stats.dwell_count == 1
    assert stats.cut_time == pytest.approx(1.0)
    assert stats.rapid_time == 0


def test_active_time_sums_moves_and_dwells_with_process_on():
    text = "M8\nG1 X10 F600\nG04 P2\nM9\nG1 X20 F600"
    result = parse_gcode(text, dialect=ARC_SECONDS)
    stats = compute_stats(Toolpath(result.moves), result.commands)
    assert stats.active_time == pytest.approx(1.0 + 2.0)

def test_dwell_in_x_is_time_not_a_coordinate():
    result = parse_gcode("G1 X10 F600\nG04 X2\nG1 Y5", dialect=ARC_SECONDS)
    dwell = result.moves[1]
    assert dwell.dwell == pytest.approx(2.0)
    assert dwell.start == dwell.end == (10.0, 0.0, 0.0)   # a ferramenta não foi para X2
    assert result.moves[-1].end == (10.0, 5.0, 0.0)


def test_dwell_in_x_is_seconds_even_when_p_is_milliseconds():
    result = parse_gcode("G04 X1.5", dialect=ARC_MILLISECONDS)
    assert result.moves[0].dwell == pytest.approx(1.5)


def test_dwell_in_u_is_seconds():
    assert parse_gcode("G04 U3", dialect=ARC_SECONDS).moves[0].dwell == pytest.approx(3.0)


def test_dwell_in_x_ignores_inches():
    result = parse_gcode("G20\nG04 X2", dialect=ARC_SECONDS)
    assert result.moves[0].dwell == pytest.approx(2.0)


def test_dwell_without_time_is_a_warning():
    result = parse_gcode("G04")
    assert [i.severity for i in result.issues] == [WARNING]