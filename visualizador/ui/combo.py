"""combo com a lista suspensa no visual e no comportamento dos menus do programa."""
from __future__ import annotations

from PySide6.QtCore import QPointF, QPropertyAnimation, QRectF, Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen, QPolygonF, QRegion
from PySide6.QtWidgets import QComboBox, QStyledItemDelegate

from ui.theme import RADIUS_MD, TEXT_MUTED, TEXT_SECONDARY

FADE_MS = 120
POPUP_RADIUS = int(RADIUS_MD.removesuffix("px"))
ARROW_HALF_WIDTH = 4
ARROW_HEIGHT = 4
ARROW_RIGHT_MARGIN = 14


class ComboBox(QComboBox):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        # sem este delegate o Qt ignora as regras ::item do tema na lista suspensa
        self.setItemDelegate(QStyledItemDelegate(self))
        self._fade: QPropertyAnimation | None = None

    def showPopup(self) -> None:
        """abre a lista com cantos arredondados e um fade curto, como os menus."""
        popup = self.view().window()
        popup.setWindowOpacity(0.0)
        super().showPopup()

        # máscara em vez de janela transparente: funciona também sem compositor (Linux antigo)
        outline = QPainterPath()
        outline.addRoundedRect(QRectF(popup.rect()), POPUP_RADIUS, POPUP_RADIUS)
        popup.setMask(QRegion(outline.toFillPolygon().toPolygon()))

        self._fade = QPropertyAnimation(popup, b"windowOpacity", self)
        self._fade.setDuration(FADE_MS)
        self._fade.setStartValue(0.0)
        self._fade.setEndValue(1.0)
        self._fade.start()

    def paintEvent(self, event) -> None:
        """desenha a seta: sem ela o combo se confunde com um campo de texto."""
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
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