"""campo numérico que só reage à roda do mouse depois de clicado."""
from __future__ import annotations

from PySide6.QtCore import QLocale, Qt
from PySide6.QtWidgets import QDoubleSpinBox

NUMBER_LOCALE = QLocale(QLocale.Language.C)


class SpinBox(QDoubleSpinBox):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setLocale(NUMBER_LOCALE)
        self.setGroupSeparatorShown(False)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def wheelEvent(self, event) -> None:
        if self.hasFocus():
            super().wheelEvent(event)
        else:
            event.ignore()