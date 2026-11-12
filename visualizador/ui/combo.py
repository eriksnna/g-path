"""combo com a lista suspensa no visual dos menus do programa."""
from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QStyledItemDelegate


class ComboBox(QComboBox):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        # sem este delegate o Qt ignora as regras ::item do tema na lista suspensa
        self.setItemDelegate(QStyledItemDelegate(self))