"""Botões de vista padrão da câmera 3D (topo, frente, lado, isométrica)."""
from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget

from core.i18n import tr
from ui.theme import SPACE_XS

_VIEWS = [
    ("top", "camera_top"),
    ("front", "camera_front"),
    ("side", "camera_side"),
    ("iso", "camera_iso"),
]


class CameraControls(QWidget):
    view_requested = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACE_XS)
        for name, key in _VIEWS:
            button = QPushButton(tr(key))
            button.setObjectName("preset")
            button.clicked.connect(lambda checked=False, n=name: self.view_requested.emit(n))
            layout.addWidget(button)