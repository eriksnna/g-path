"""fundo da tela inicial: grade em perspectiva e um percurso que se desenha sozinho.

leve: a grade é desenhada uma vez por tamanho de janela e guardada
em um pixmap; a cada quadro só se desenham uma polilinha e um ponto.
"""
from __future__ import annotations

import math

from PySide6.QtCore import QElapsedTimer, QPointF, QRect, QTimer, Qt
from PySide6.QtGui import QBrush, QColor, QLinearGradient, QPainter, QPen, QPixmap, QPolygonF
from PySide6.QtWidgets import QWidget

from ui.theme import ACCENT, BORDER, BORDER_STRONG, SURFACE_0

FRAME_MS = 33            # 30 quadros por segundo
DRAW_SECONDS = 16.0      # tempo para desenhar o percurso inteiro
HOLD_SECONDS = 3.0       # pausa com o percurso completo antes de recomeçar
FADE_SECONDS = 1.2       # no fim da pausa, o percurso some aos poucos
HORIZON = 0.60           # altura do horizonte, como fração da janela
LAYERS = 7
LAYER_HEIGHT = 0.08
GRID_FADE = 0.6          # fração do chão, a partir do fundo, em que a grade vai surgindo
DIRTY_MARGIN = 8         # folga em volta do percurso na área redesenhada a cada quadro
DEPTH_FACTOR = 2.4       # quanto o fundo "encolhe" em relação à frente
HALF_WIDTH = 0.62        # meia largura do chão na frente, como fração da janela
HEIGHT_SCALE = 0.55      # altura de 1 unidade de Z, como fração da área do chão
GRID_X = [i / 5 for i in range(-9, 10)]     # linhas que vão para o fundo
GRID_DEPTH = [i / 10 for i in range(0, 11)]  # linhas horizontais
LAYERS = 6
LAYER_HEIGHT = 0.09
WALL = [(-0.42, 0.10), (0.42, 0.10), (0.42, 0.38), (-0.42, 0.38)]  # contorno (x, profundidade)
TOOL_RADIUS = 3.5


def _toolpath_points() -> list[tuple[float, float, float]]:
    """parede em camadas, como em uma deposição: contorno fechado, sobe, repete."""
    points = []
    for layer in range(LAYERS):
        z = layer * LAYER_HEIGHT
        points += [(x, depth, z) for x, depth in WALL]
        points.append((*WALL[0], z))
    return points


class StartBackground(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._grid: QPixmap | None = None
        self._path: list[QPointF] = []
        self._lengths: list[float] = []  # comprimento acumulado até cada ponto
        self._dirty = QRect()            # única área que muda entre um quadro e outro
        self._clock = QElapsedTimer()
        self._clock.start()
        self._timer = QTimer(self)
        self._timer.setInterval(FRAME_MS)
        self._timer.timeout.connect(lambda: self.update(self._dirty))

    # só anima enquanto a tela inicial está visível
    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._timer.start()

    def hideEvent(self, event) -> None:
        super().hideEvent(event)
        self._timer.stop()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._rebuild()

    def _project(self, x: float, depth: float, z: float = 0.0) -> QPointF:
        """ponto do chão (x, profundidade 0..1, altura) para a tela."""
        w, h = self.width(), self.height()
        scale = 1.0 / (1.0 + depth * DEPTH_FACTOR)
        floor = h * (1.0 - HORIZON)
        return QPointF(
            w / 2 + x * w * HALF_WIDTH * scale,
            h * HORIZON + floor * scale - z * floor * HEIGHT_SCALE * scale,
        )

    def _rebuild(self) -> None:
        if self.width() <= 0 or self.height() <= 0:
            return
        ratio = self.devicePixelRatioF()
        grid = QPixmap(self.size() * ratio)
        grid.setDevicePixelRatio(ratio)
        grid.fill(QColor(SURFACE_0))
        painter = QPainter(grid)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor(BORDER), 1))
        for x in GRID_X:
            painter.drawLine(self._project(x, 0.0), self._project(x, 1.0))
        for depth in GRID_DEPTH:
            painter.drawLine(self._project(GRID_X[0], depth), self._project(GRID_X[-1], depth))
        # a grade surge aos poucos a partir do fundo, em vez de terminar numa borda seca
        far = self._project(0.0, 1.0).y()
        fade = QLinearGradient(0, far, 0, far + (self.height() - far) * GRID_FADE)
        fade.setColorAt(0.0, QColor(SURFACE_0))
        transparent = QColor(SURFACE_0)
        transparent.setAlpha(0)
        fade.setColorAt(1.0, transparent)
        painter.fillRect(0, int(far) - 2, self.width(), self.height(), QBrush(fade))
        painter.end()
        self._grid = grid

        self._path = [self._project(*point) for point in _toolpath_points()]
        self._lengths = [0.0]
        for a, b in zip(self._path, self._path[1:]):
            self._lengths.append(self._lengths[-1] + math.hypot(b.x() - a.x(), b.y() - a.y()))
        self._dirty = QPolygonF(self._path).boundingRect().toAlignedRect().adjusted(
            -DIRTY_MARGIN, -DIRTY_MARGIN, DIRTY_MARGIN, DIRTY_MARGIN)
        self.update()

    def _cycle_seconds(self) -> float:
        return (self._clock.elapsed() / 1000.0) % (DRAW_SECONDS + HOLD_SECONDS)

    def _opacity(self, seconds: float) -> float:
        """1 durante o desenho e a pausa; cai até 0 no último trecho do ciclo."""
        remaining = DRAW_SECONDS + HOLD_SECONDS - seconds
        return min(remaining / FADE_SECONDS, 1.0)

    def _drawn_part(self, seconds: float) -> list[QPointF]:
        """Trecho do percurso já desenhado no instante dado."""
        target = min(seconds / DRAW_SECONDS, 1.0) * self._lengths[-1]
        drawn = [self._path[0]]
        for i in range(1, len(self._path)):
            if self._lengths[i] <= target:
                drawn.append(self._path[i])
                continue
            a, b = self._path[i - 1], self._path[i]
            span = self._lengths[i] - self._lengths[i - 1]
            t = (target - self._lengths[i - 1]) / span if span > 0 else 0.0
            drawn.append(QPointF(a.x() + t * (b.x() - a.x()), a.y() + t * (b.y() - a.y())))
            break
        return drawn

    def paintEvent(self, event) -> None:
        if self._grid is None or len(self._path) < 2 or len(self._lengths) != len(self._path):
            return
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self._grid)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        seconds = self._cycle_seconds()
        painter.setOpacity(self._opacity(seconds))
        drawn = self._drawn_part(seconds)
        painter.setPen(QPen(QColor(BORDER_STRONG), 1.4))
        painter.drawPolyline(QPolygonF(drawn))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(ACCENT))
        painter.drawEllipse(drawn[-1], TOOL_RADIUS, TOOL_RADIUS)
        painter.end()