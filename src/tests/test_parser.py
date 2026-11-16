import math

import pytest

from core.parser import ERROR, WARNING, arc_points, clean_line, parse_gcode

def test_clean_line_removes_comments_and_normalizes():
    assert clean_line("g1 x10 (lateral) ; fim") == "G1 X10"


def test_g1_after_g0_default_is_rapid_then_cut():
    result = parse_gcode("G1 X10 Y0 F300")
    move = result.moves[0]
    assert move.is_cut
    assert move.start == (0, 0, 0)
    assert move.end == (10, 0, 0)


def test_g0_is_rapid():
    result = parse_gcode("G0 X10")
    assert not result.moves[0].is_cut


def test_incremental_mode_accumulates_position():
    result = parse_gcode("G91\nG1 X5\nG1 X5")
    assert result.moves[-1].end == (10, 0, 0)


def test_inches_are_converted_to_mm_including_feed():
    result = parse_gcode("G20 G1 X1 F10")
    move = result.moves[0]
    assert move.end[0] == pytest.approx(25.4)
    assert move.feed == pytest.approx(254.0)


def test_zero_length_move_is_ignored():
    assert parse_gcode("G1 X0 Y0").moves == []


def test_arc_ends_exactly_at_target_and_keeps_radius():
    result = parse_gcode("G1 X50\nG3 X0 Y50 I-50 J0")
    arc_moves = result.moves[1:]
    assert arc_moves[-1].end == (0.0, 50.0, 0.0)
    for move in arc_moves:
        assert math.hypot(move.end[0], move.end[1]) == pytest.approx(50.0)


def test_cw_and_ccw_take_opposite_directions():
    ccw = arc_points((50, 0, 0), (0, 50, 0), (0, 0), clockwise=False)
    cw = arc_points((50, 0, 0), (0, 50, 0), (0, 0), clockwise=True)
    assert ccw[len(ccw) // 2][1] > 0    # G3 passa pelo primeiro quadrante
    assert cw[len(cw) // 2][1] < 0      # G2 dá a volta pelo terceiro quadrante


def _arc_middle(text):
    moves = parse_gcode(text).moves[1:]  # o primeiro movimento é o G1 de posicionamento
    return moves[len(moves) // 2 - 1].end


def test_arc_with_positive_r_matches_the_same_arc_with_ij():
    with_r = parse_gcode("G1 X50 F100\nG3 X0 Y50 R50").moves
    with_ij = parse_gcode("G1 X50 F100\nG3 X0 Y50 I-50 J0").moves
    assert len(with_r) == len(with_ij)
    for a, b in zip(with_r, with_ij):
        assert a.end == pytest.approx(b.end, abs=1e-9)


def test_g2_and_g3_with_r_bulge_to_opposite_sides():
    ccw = _arc_middle("G1 X50 F100\nG3 X0 Y50 R50")
    cw = _arc_middle("G1 X50 F100\nG2 X0 Y50 R50")
    assert math.hypot(ccw[0], ccw[1]) == pytest.approx(50)            # centro na origem
    assert math.hypot(cw[0] - 50, cw[1] - 50) == pytest.approx(50)    # centro em (50, 50)


def test_negative_r_takes_the_long_way_round():
    short = parse_gcode("G1 X50 F100\nG3 X0 Y50 R50").moves[1:]
    long = parse_gcode("G1 X50 F100\nG3 X0 Y50 R-50").moves[1:]
    assert len(long) == 3 * len(short)   # 270 graus contra 90
    assert long[-1].end == (0.0, 50.0, 0.0)


def test_half_circle_with_r_has_center_on_the_chord():
    middle = _arc_middle("G1 X10 F100\nG3 X-10 Y0 R10")
    assert middle == pytest.approx((0.0, 10.0, 0.0), abs=1e-9)


def test_r_slightly_short_from_rounding_is_accepted():
    result = parse_gcode("G1 X30 Y10 F100\nG3 X10 Y10 R9.995")
    assert not [i for i in result.issues if i.severity == ERROR]


def test_r_too_small_is_an_error_on_its_line():
    result = parse_gcode("G1 X10 F100\nG2 X0 Y10 R5")
    assert len(result.moves) == 1
    errors = [i for i in result.issues if i.severity == ERROR]
    assert len(errors) == 1 and errors[0].line == 2


def test_full_circle_with_r_is_an_error():
    result = parse_gcode("G1 X10 F100\nG2 X10 Y0 R5")
    assert len(result.moves) == 1
    assert [i.line for i in result.issues if i.severity == ERROR] == [2]


def test_r_in_inches_is_converted():
    moves = parse_gcode("G20\nG1 X1 F10\nG3 X0 Y1 R1").moves
    assert moves[-1].end == pytest.approx((0.0, 25.4, 0.0))
    assert math.hypot(*moves[len(moves) // 2].end[:2]) == pytest.approx(25.4)

def test_multiple_g_codes_on_same_line_are_all_applied():
    result = parse_gcode("G91 G1 X5")
    assert result.moves[0].end == (5, 0, 0)

def test_missing_feed_warns_once_at_first_cut():
    result = parse_gcode("G1 X10\nG1 X20")
    feed_issues = [i for i in result.issues if "F ausente" in i.message]
    assert len(feed_issues) == 1
    assert feed_issues[0].line == 1
    assert feed_issues[0].severity == WARNING


def test_rapid_without_feed_does_not_warn():
    assert parse_gcode("G0 X10").issues == []


def test_move_outside_work_area_is_reported_once_per_line():
    limits = {"X": (0, 300), "Y": (0, 200), "Z": (-100, 100)}
    result = parse_gcode("G1 X400 Y400 F100", limits=limits)
    bounds = [i for i in result.issues if "área de trabalho" in i.message]
    assert len(bounds) == 1
    assert bounds[0].line == 1
    assert bounds[0].severity == ERROR


def test_moves_have_their_source_line():
    result = parse_gcode("G21\n\nG1 X10 F100\nG1 X20 F100")
    assert [m.line for m in result.moves] == [3, 4]