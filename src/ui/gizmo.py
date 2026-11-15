"""gizmo de orientação no canto do viewport: mostra os eixos e alinha a vista com um clique."""
from __future__ import annotations

import math

from PySide6.QtCore import QEvent, QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget

from core.i18n import tr
from core.orientation import project_axes
from ui.theme import AXIS_X, AXIS_Y, AXIS_Z, BORDER, SPACE_LG, SURFACE_0, SURFACE_1

GIZMO_SIZE = 92
GIZMO_MARGIN = SPACE_LG
AXIS_LENGTH = 30.0
TIP_RADIUS = 9.0
LABEL_PX = 10
BACK_ALPHA = 110  # eixo que aponta para longe da câmera fica esmaecido
DEFAULT_VIEW = "iso"
# rótulo, cor e vista padrão que o clique na ponta pede
_AXES = (("X", AXIS_X, "side"), ("Y", AXIS_Y, "front"), ("Z", AXIS_Z, "top"))


class ViewGizmo(QWidget):
    view_requested = Signal(str)

    def __init__(self, viewport) -> None:
        super().__init__(viewport)
        self._viewport = viewport
        self._angles: tuple[float, float] | None = None
        self.setFixedSize(GIZMO_SIZE, GIZMO_SIZE)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(tr("gizmo_tooltip"))
        viewport.installEventFilter(self)
        viewport.camera_changed.connect(self._on_camera_changed)
        self._place()

    def eventFilter(self, watched, event) -> bool:
        if event.type() == QEvent.Type.Resize:
            self._place()
        return False

    def _place(self) -> None:
        parent = self.parentWidget()
        self.move(parent.width() - GIZMO_SIZE - GIZMO_MARGIN, parent.height() - GIZMO_SIZE - GIZMO_MARGIN)

    def _camera_angles(self) -> tuple[float, float]:
        opts = self._viewport.opts
        return float(opts["elevation"]), float(opts["azimuth"])

    def _on_camera_changed(self) -> None:
        angles = self._camera_angles()
        if angles != self._angles:
            self.update()

    def _tips(self) -> list[tuple[float, QPointF, str, str, str]]:
        """pontas dos eixos na tela, da mais distante para a mais próxima da câmera."""
        self._angles = self._camera_angles()
        middle = GIZMO_SIZE / 2
        tips = []
        for (right, up, depth), (label, color, view) in zip(project_axes(*self._angles), _AXES):
            point = QPointF(middle + right * AXIS_LENGTH, middle - up * AXIS_LENGTH)
            tips.append((depth, point, label, color, view))
        return sorted(tips, key=lambda tip: tip[0])

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        center = QPointF(GIZMO_SIZE / 2, GIZMO_SIZE / 2)

        painter.setPen(QPen(QColor(BORDER), 1))
        painter.setBrush(QColor(SURFACE_1))
        painter.drawEllipse(center, GIZMO_SIZE / 2 - 1, GIZMO_SIZE / 2 - 1)

        font = painter.font()
        font.setPixelSize(LABEL_PX)
        font.setBold(True)
        painter.setFont(font)

        for depth, tip, label, color, _view in self._tips():
            shade = QColor(color)
            if depth < 0:
                shade.setAlpha(BACK_ALPHA)
            painter.setPen(QPen(shade, 2))
            painter.drawLine(center, tip)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(shade)
            painter.drawEllipse(tip, TIP_RADIUS, TIP_RADIUS)
            painter.setPen(QColor(SURFACE_0))
            box = QRectF(tip.x() - TIP_RADIUS, tip.y() - TIP_RADIUS, 2 * TIP_RADIUS, 2 * TIP_RADIUS)
            painter.drawText(box, Qt.AlignmentFlag.AlignCenter, label)
        painter.end()

    def mousePressEvent(self, event) -> None:
        if event.button() != Qt.MouseButton.LeftButton:
            return
        click = event.position()
        # a ponta mais próxima da câmera ganha quando duas se sobrepõem
        for _depth, tip, _label, _color, view in reversed(self._tips()):
            if math.hypot(click.x() - tip.x(), click.y() - tip.y()) <= TIP_RADIUS:
                self.view_requested.emit(view)
                return
        self.view_requested.emit(DEFAULT_VIEW)