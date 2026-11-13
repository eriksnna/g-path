import pytest

from core.layers import depth_levels
from core.lexer import WARNING, Issue
from core.parser import parse_gcode
from core.timeline import build_marks, step_layer, step_move
from core.toolpath import Toolpath

PROGRAM = """G1 X0 Y0 Z0 F600
M3
G1 X10
G1 Z1
G1 X0
M5
G0 X20
"""


@pytest.fixture
def toolpath():
    return Toolpath(parse_gcode(PROGRAM).moves)


def test_active_span_covers_moves_with_process_on(toolpath):
    marks = build_marks(toolpath, depth_levels(toolpath))
    assert marks.active_spans == [(toolpath.cum_start[0], toolpath.cum_end[2])]


def test_layer_starts_and_layer_at(toolpath):
    marks = build_marks(toolpath, depth_levels(toolpath))
    assert list(marks.layer_starts) == [toolpath.cum_start[0], toolpath.cum_start[1]]
    assert marks.layer_at(0.0) == 1
    assert marks.layer_at(toolpath.total_time) == 2


def test_issue_marks_use_line_time(toolpath):
    marks = build_marks(toolpath, depth_levels(toolpath), [Issue(5, WARNING, "x")])
    assert marks.issues == [(toolpath.cum_start[2], WARNING)]


def test_step_move_both_directions(toolpath):
    t1 = toolpath.cum_start[1]
    assert step_move(toolpath, 0.0, 1) == t1
    assert step_move(toolpath, t1, -1) == 0.0
    assert step_move(toolpath, toolpath.total_time, 1) == toolpath.total_time


def test_step_layer_falls_back_to_ends(toolpath):
    marks = build_marks(toolpath, depth_levels(toolpath))
    assert step_layer(marks, 0.0, 1) == marks.layer_starts[1]
    assert step_layer(marks, marks.layer_starts[1], 1) == marks.total
    assert step_layer(marks, 0.0, -1) == 0.0