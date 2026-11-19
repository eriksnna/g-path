"""cores do percurso durante a reprodução. só numpy: dá para testar sem abrir a interface."""
from __future__ import annotations

import numpy as np

VERTICES_PER_MOVE = 2  # cada movimento é uma reta: início e fim


class ProgressColors:
    """cores por vértice das duas linhas (trabalho e deslocamento), no formato do GLLinePlotItem.
    entre um quadro e outro, só repinta os movimentos que passaram de 'a fazer' para 'feito'
    (ou o contrário, ao voltar): o custo deixa de crescer com o tamanho do programa."""

    def __init__(self, is_cut: np.ndarray, dim: np.ndarray, bright: np.ndarray,
                 hidden: np.ndarray | None = None) -> None:
        dim, bright = dim.copy(), bright.copy()
        if hidden is not None:
            dim[hidden, 3] = 0.0
            bright[hidden, 3] = 0.0
        # quantos movimentos de trabalho existem antes de cada índice: traduz um índice do
        # programa para as posições correspondentes nas duas linhas
        self._cut_before = np.concatenate(([0], np.cumsum(is_cut)))
        self._dim = (_per_vertex(dim[is_cut]), _per_vertex(dim[~is_cut]))
        self._bright = (_per_vertex(bright[is_cut]), _per_vertex(bright[~is_cut]))
        self.cut = self._dim[0].copy()
        self.rapid = self._dim[1].copy()
        self._started = 0

    def update(self, started: int) -> bool:
        """marca como feitos os primeiros `started` movimentos. devolve True se algo mudou."""
        low, high = sorted((self._started, started))
        if low == high:
            return False
        source_cut, source_rapid = self._bright if started > self._started else self._dim
        c0, c1 = VERTICES_PER_MOVE * self._cut_before[low], VERTICES_PER_MOVE * self._cut_before[high]
        r0, r1 = VERTICES_PER_MOVE * low - c0, VERTICES_PER_MOVE * high - c1
        self.cut[c0:c1] = source_cut[c0:c1]
        self.rapid[r0:r1] = source_rapid[r0:r1]
        self._started = started
        return True


def _per_vertex(colors: np.ndarray) -> np.ndarray:
    return np.repeat(colors, VERTICES_PER_MOVE, axis=0)