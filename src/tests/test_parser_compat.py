import math

import pytest

from core.parser import ERROR, WARNING, parse_gcode


def _ends(result):
    return [m.end for m in result.moves]


def test_program_number_header_is_main_program():
    text = "%\nO0001 (PECA)\nG21 G90\nG1 X10 F200\nG1 Y10\nM30\n%"
    result = parse_gcode(text)
    assert _ends(result) == [(10.0, 0.0, 0.0), (10.0, 10.0, 0.0)]
    assert result.issues == []


def test_called_label_is_still_a_subroutine():
    text = "G1 X0 F100\nM98 P100 L2\nM30\nO100\nG91 G1 X5\nG90\nM99"
    assert _ends(parse_gcode(text))[-1] == (10.0, 0.0, 0.0)


def test_g92_shifts_coordinates_without_moving():
    result = parse_gcode("G1 X10 F100\nG92 X0\nG1 X5")
    assert _ends(result) == [(10.0, 0.0, 0.0), (15.0, 0.0, 0.0)]


def test_g28_is_warned_and_not_drawn():
    result = parse_gcode("G1 X10 F100\nG28 X0 Y0")
    assert len(result.moves) == 1
    assert [(i.line, i.severity) for i in result.issues] == [(2, WARNING)]


def test_unknown_g_code_warns_once():
    result = parse_gcode("G1 X1 F100\nG38\nG38")
    assert [i.line for i in result.issues] == [2]


def test_arc_without_center_is_error():
    result = parse_gcode("G1 X0 Y0 F100\nG2 X10 Y0")
    assert [(i.line, i.severity) for i in result.issues] == [(2, ERROR)]


def _middle(moves):
    return moves[len(moves) // 2].end


def test_g18_arc_uses_i_and_k_in_the_xz_plane():
    moves = parse_gcode("G18\nG1 X10 F100\nG3 X0 Z10 I-10 K0").moves[1:]
    assert moves[-1].end == (0.0, 0.0, 10.0)
    for move in moves:
        assert move.end[1] == 0.0                                     # não sai do plano XZ
        assert math.hypot(move.end[0], move.end[2]) == pytest.approx(10.0)


def test_g18_direction_is_seen_from_positive_y():
    # visto de +Y, Z aponta para a direita e X para cima: de X10 a Z10 o G2 passa pelo
    # primeiro quadrante (X e Z positivos) e o G3 dá a volta pelo lado oposto
    cw = _middle(parse_gcode("G18\nG1 X10 F100\nG2 X0 Z10 I-10 K0").moves[1:])
    ccw = _middle(parse_gcode("G18\nG1 X10 F100\nG3 X0 Z10 I-10 K0").moves[1:])
    assert cw[0] > 0 and cw[2] > 0
    assert ccw[0] < 0 or ccw[2] < 0


def test_g19_arc_uses_j_and_k_in_the_yz_plane():
    moves = parse_gcode("G19\nG1 Y10 F100\nG3 Y0 Z10 J-10 K0").moves[1:]
    assert moves[-1].end == (0.0, 0.0, 10.0)
    assert all(move.end[0] == 0.0 for move in moves)
    middle = _middle(moves)
    assert middle[1] > 0 and middle[2] > 0                            # visto de +X, como no G17


def test_g18_helix_advances_along_y():
    moves = parse_gcode("G18\nG1 X10 F100\nG3 X10 Y6 Z0 I-10 K0").moves[1:]
    assert moves[-1].end == (10.0, 6.0, 0.0)
    assert len(moves) > 10


def test_g18_arc_with_r():
    moves = parse_gcode("G18\nG1 X10 F100\nG2 X0 Z10 R10").moves[1:]
    assert all(math.hypot(m.end[0], m.end[2]) == pytest.approx(10.0) for m in moves)


def test_arc_without_center_names_the_plane_letters():
    result = parse_gcode("G18\nG1 X10 F100\nG2 X0 Z10")
    errors = [i for i in result.issues if i.severity == ERROR]
    assert len(errors) == 1 and "I/K" in errors[0].message