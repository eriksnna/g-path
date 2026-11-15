"""moldura flutuante presa ao canto superior direito do viewport, para controles da vista."""
from __future__ import annotations

from PySide6.QtCore import QEvent
from PySide6.QtWidgets import QFrame, QHBoxLayout, QWidget

from ui.theme import SPACE_LG, SPACE_MD, SPACE_XS

OVERLAY_MARGIN = SPACE_LG


class CornerOverlay(QFrame):
    def __init__(self, viewport: QWidget, content: QWidget) -> None:
        super().__init__(viewport)
        self.setObjectName("dro")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(SPACE_MD, SPACE_XS, SPACE_MD, SPACE_XS)
        layout.addWidget(content)
        viewport.installEventFilter(self)
        self._place()

    def eventFilter(self, watched, event) -> bool:
        if event.type() == QEvent.Type.Resize:
            self._place()
        return False

    def event(self, event) -> bool:
        handled = super().event(event)
        # o conteúdo mudou de tamanho (ex.: lista de camadas): reajusta e reposiciona
        if event.type() == QEvent.Type.LayoutRequest:
            self._place()
        return handled

    def _place(self) -> None:
        self.adjustSize()
        self.move(self.parentWidget().width() - self.width() - OVERLAY_MARGIN, OVERLAY_MARGIN)