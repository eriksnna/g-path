import pytest

from core.cycles import CHIP_BREAK_RETRACT, PECK_CLEARANCE
from core.parser import ERROR, parse_gcode

START = "G90 G0 X0 Y0 Z10 F100\n"


def _points(text):
    moves = parse_gcode(START + text).moves[1:]  # sem o posicionamento inicial
    return [m.end for m in moves], moves


def test_g81_drills_each_position_and_returns_to_initial_level():
    ends, moves = _points("G81 X10 Y5 Z-3 R2\nX20\nG80")
    assert ends == [
        (10, 5, 10), (10, 5, 2), (10, 5, -3), (10, 5, 10),
        (20, 5, 10), (20, 5, 2), (20, 5, -3), (20, 5, 10),
    ]
    assert [m.is_cut for m in moves] == [False, False, True, False] * 2


def test_g99_returns_only_to_r_plane():
    ends, _ = _points("G99 G81 X10 Y0 Z-3 R2\nX20")
    assert ends[3] == (10, 0, 2)
    assert ends[4] == (20, 0, 2)


def test_g80_and_g0_end_the_cycle():
    ends, _ = _points("G81 X10 Y0 Z-3 R2\nG80\nX30")
    assert ends[-1] == (30, 0, 10)          # depois do G80, X30 é um movimento comum
    ends, _ = _points("G81 X10 Y0 Z-3 R2\nG0 X30")
    assert ends[-1] == (30, 0, 10)


def test_line_without_position_only_sets_parameters():
    ends, _ = _points("G81 Z-3 R2\nX10 Y0")
    assert ends == [(10, 0, 10), (10, 0, 2), (10, 0, -3), (10, 0, 10)]


def test_g82_dwells_at_the_bottom():
    _, moves = _points("G82 X10 Y0 Z-3 R2 P1.5")
    dwell = [m for m in moves if m.dwell]
    assert len(dwell) == 1
    assert dwell[0].dwell == pytest.approx(1.5) and dwell[0].end == (10, 0, -3)


def test_g83_pecks_back_to_r_between_steps():
    ends, _ = _points("G83 X0 Y0 Z-6 R2 Q4")
    zs = [z for _, _, z in ends]
    assert zs == [2, -2, 2, -2 + PECK_CLEARANCE, -6, 10]


def test_g73_only_backs_off_a_little():
    ends, _ = _points("G73 X0 Y0 Z-6 R2 Q4")
    zs = [z for _, _, z in ends]
    assert zs == [2, -2, -2 + CHIP_BREAK_RETRACT, -6, 10]


def test_incremental_r_and_z_are_relative():
    ends, _ = _points("G91 G81 X10 Y0 Z-5 R-8")
    assert ends[1] == (10, 0, 2) and ends[2] == (10, 0, -3)


def test_inches_are_converted():
    moves = parse_gcode("G20 G90 G0 X0 Y0 Z1\nG81 X1 Y0 Z-0.1 R0.1 F4").moves
    assert moves[-2].end == pytest.approx((25.4, 0, -2.54))


@pytest.mark.parametrize("text", [
    "G81 X10 Y0 Z-3",            # sem R
    "G83 X10 Y0 Z-3 R2",         # sem Q
    "G81 X10 Y0 Z5 R2",          # fundo acima do R
])
def test_invalid_cycles_are_errors_on_their_line(text):
    result = parse_gcode(START + text)
    assert [(i.line, i.severity) for i in result.issues] == [(2, ERROR)]


def test_cycle_counts_holes_by_code():
    result = parse_gcode(START + "G81 X10 Y0 Z-3 R2\nX20\nG83 X30 Z-3 R2 Q1")
    assert result.commands["G81"] == 2 and result.commands["G83"] == 1