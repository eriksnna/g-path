"""combo construído sobre QMenu: mesma lista suspensa do menu de velocidade.

oferece os métodos de QComboBox que o programa usa, para servir de substituto direto. -> linux proof (eu acho)
"""
from __future__ import annotations

from PySide6.QtCore import QPointF, QSize, Qt, Signal
from PySide6.QtGui import QColor, QPainter, QPen, QPolygonF
from PySide6.QtWidgets import QMenu, QPushButton

from ui.theme import TEXT_MUTED, TEXT_PRIMARY, TEXT_SECONDARY

TEXT_PADDING = 12        # espaço entre o texto e as bordas laterais
ARROW_SPACE = 22         # faixa reservada à seta, à direita
ARROW_HALF_WIDTH = 4
ARROW_HEIGHT = 4
ARROW_RIGHT_MARGIN = 14
NO_ITEM = -1


class ComboBox(QPushButton):
    currentIndexChanged = Signal(int)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("combo")
        self.setFocusPolicy(Qt.FocusPolicy.TabFocus)  # um clique não rouba os atalhos de reprodução
        self._items: list[tuple[str, object]] = []
        self._index = NO_ITEM
        self._menu = QMenu(self)
        self._menu.aboutToShow.connect(self._fill_menu)
        self.setMenu(self._menu)

    # --- mesmos nomes de QComboBox ---

    def addItem(self, text: str, data: object = None) -> None:
        self._items.append((text, data))
        self.updateGeometry()
        if self._index == NO_ITEM:
            self._select(0)

    def removeItem(self, index: int) -> None:
        if not 0 <= index < len(self._items):
            return
        del self._items[index]
        self.updateGeometry()
        if index < self._index:
            self._select(self._index - 1)
        elif index == self._index:
            self._select(min(index, len(self._items) - 1), force=True)

    def clear(self) -> None:
        self._items.clear()
        self.updateGeometry()
        self._select(NO_ITEM)

    def count(self) -> int:
        return len(self._items)

    def currentIndex(self) -> int:
        return self._index

    def setCurrentIndex(self, index: int) -> None:
        if index == NO_ITEM or 0 <= index < len(self._items):
            self._select(index)

    def currentText(self) -> str:
        return self._items[self._index][0] if self._index != NO_ITEM else ""

    def currentData(self) -> object:
        return self.itemData(self._index)

    def itemData(self, index: int) -> object:
        return self._items[index][1] if 0 <= index < len(self._items) else None

    def findData(self, data: object) -> int:
        for index, (_, item_data) in enumerate(self._items):
            if item_data == data:
                return index
        return NO_ITEM

    # --- interno ---

    def _select(self, index: int, force: bool = False) -> None:
        """force: o índice é o mesmo, mas o item naquela posição mudou."""
        changed = index != self._index
        self._index = index
        self.setAccessibleName(self.currentText())
        self.update()  # o texto é desenhado em paintEvent, com margem própria
        if changed or force:
            self.currentIndexChanged.emit(index)

    def _fill_menu(self) -> None:
        self._menu.clear()
        self._menu.setMinimumWidth(self.width())
        for index, (text, _) in enumerate(self._items):
            action = self._menu.addAction(text)
            action.setCheckable(True)
            action.setChecked(index == self._index)
            action.triggered.connect(lambda _checked=False, i=index: self._select(i))

    def sizeHint(self) -> QSize:
        """Largura do maior item, para o combo não mudar de tamanho a cada escolha."""
        hint = super().sizeHint()
        metrics = self.fontMetrics()
        widest = max((metrics.horizontalAdvance(text) for text, _ in self._items), default=0)
        return QSize(max(hint.width(), widest + 2 * TEXT_PADDING + ARROW_SPACE), hint.height())

    def minimumSizeHint(self) -> QSize:
        return self.sizeHint()

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        text_rect = self.rect().adjusted(TEXT_PADDING, 0, -ARROW_SPACE, 0)
        text = self.fontMetrics().elidedText(
            self.currentText(), Qt.TextElideMode.ElideRight, text_rect.width())
        painter.setPen(QColor(TEXT_PRIMARY if self.isEnabled() else TEXT_MUTED))
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, text)
        color = TEXT_SECONDARY if self.isEnabled() else TEXT_MUTED
        painter.setPen(QPen(QColor(color), 1.5, Qt.PenStyle.SolidLine,
                            Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        x = self.width() - ARROW_RIGHT_MARGIN
        y = self.height() / 2
        painter.drawPolyline(QPolygonF([
            QPointF(x - ARROW_HALF_WIDTH, y - ARROW_HEIGHT / 2),
            QPointF(x, y + ARROW_HEIGHT / 2),
            QPointF(x + ARROW_HALF_WIDTH, y - ARROW_HEIGHT / 2),
        ]))
        painter.end()