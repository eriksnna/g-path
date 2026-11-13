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
    result = parse_gcode("G1 X1 F100\nG99\nG99")
    assert [i.line for i in result.issues] == [2]


def test_arc_without_center_is_error():
    result = parse_gcode("G1 X0 Y0 F100\nG2 X10 Y0")
    assert [(i.line, i.severity) for i in result.issues] == [(2, ERROR)]


def test_arc_outside_xy_plane_is_error():
    result = parse_gcode("G18\nG1 X0 F100\nG2 X10 Z0 I5")
    assert any(i.severity == ERROR and i.line == 3 for i in result.issues)