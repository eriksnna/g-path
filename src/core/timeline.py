"""marcas da timeline e navegação por movimento/camada."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

import numpy as np

from core.layers import layer_indices
from core.lexer import Issue
from core.toolpath import Toolpath


@dataclass(frozen=True)
class TimelineMarks:
    """tudo em segundos de simulação; a interface converte para posição na barra."""
    total: float = 0.0
    active_spans: list[tuple[float, float]] = field(default_factory=list)
    layer_starts: np.ndarray = field(default_factory=lambda: np.empty(0))
    issues: list[tuple[float, str]] = field(default_factory=list)  # (instante, severidade)

    def layer_at(self, t: float) -> int:
        """número da passada de camada em curso (1..N); 0 antes da primeira."""
        return int(np.searchsorted(self.layer_starts, t, side="right"))


def build_marks(toolpath: Toolpath, levels: Sequence[float],
                issues: Sequence[Issue] = ()) -> TimelineMarks:
    return TimelineMarks(
        total=toolpath.total_time,
        active_spans=_active_spans(toolpath),
        layer_starts=_layer_starts(toolpath, np.asarray(levels, dtype=float)),
        issues=_issue_times(toolpath, issues),
    )


def step_move(toolpath: Toolpath, t: float, direction: int) -> float:
    """início do próximo movimento (direction=1) ou do anterior (-1)."""
    return _step(toolpath.cum_start, t, direction, toolpath.total_time)


def step_layer(marks: TimelineMarks, t: float, direction: int) -> float:
    """início da próxima camada ou da anterior."""
    return _step(marks.layer_starts, t, direction, marks.total)


def _step(starts: np.ndarray, t: float, direction: int, total: float) -> float:
    if direction > 0:
        i = int(np.searchsorted(starts, t, side="right"))
        return float(starts[i]) if i < starts.size else total
    i = int(np.searchsorted(starts, t, side="left")) - 1
    return float(starts[i]) if i >= 0 else 0.0


def _active_spans(toolpath: Toolpath) -> list[tuple[float, float]]:
    active = toolpath.active.astype(np.int8)
    edges = np.diff(np.concatenate(([0], active, [0])))
    first = np.flatnonzero(edges == 1)
    last = np.flatnonzero(edges == -1) - 1
    return [(float(toolpath.cum_start[a]), float(toolpath.cum_end[b])) for a, b in zip(first, last)]


def _layer_starts(toolpath: Toolpath, levels: np.ndarray) -> np.ndarray:
    cuts = np.flatnonzero(toolpath.is_cut)
    if cuts.size == 0 or levels.size == 0:
        return np.empty(0)
    layer = layer_indices(toolpath, levels)[cuts]
    changed = np.concatenate(([True], layer[1:] != layer[:-1]))
    return toolpath.cum_start[cuts[changed]]


def _issue_times(toolpath: Toolpath, issues: Sequence[Issue]) -> list[tuple[float, str]]:
    marks = []
    for issue in issues:
        t = toolpath.time_at_line(issue.line)
        if t is not None:
            marks.append((t, issue.severity))
    return marks