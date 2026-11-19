"""widgets pequenos e genéricos usados na janela principal."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel

from ui.text import plain_tooltip


def vsep() -> QFrame:
    """linha vertical fina pra separar grupos de controles na barra superior."""
    line = QFrame()
    line.setObjectName("headerSeparator")
    line.setFixedWidth(1)
    return line


class ElidingLabel(QLabel):
    """rótulo de uma linha que corta o meio do texto quando falta espaço; o texto inteiro fica na dica."""

    def __init__(self, text: str = "", parent=None) -> None:
        super().__init__(parent)
        self._full_text = text
        self._tooltip = text
        self.setTextFormat(Qt.TextFormat.PlainText)
        self.setMinimumWidth(140)
        super().setText(text)

    def setText(self, text: str, tooltip: str | None = None) -> None:
        self._full_text = text
        self._tooltip = tooltip or text
        self._update_elided_text()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._update_elided_text()

    def _update_elided_text(self) -> None:
        elided = self.fontMetrics().elidedText(
            self._full_text, Qt.TextElideMode.ElideMiddle, self.width()
        )
        super().setText(elided)
        self.setToolTip(plain_tooltip(self._tooltip))