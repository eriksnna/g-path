"""leitura digital (DRO) sobreposta ao viewport: posição, avanço e estado do processo."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel

from core.i18n import tr
from ui.theme import ACCENT_TEXT, SPACE_LG, SPACE_SM, SPACE_XXS, TEXT_MUTED

AXES = ("X", "Y", "Z")
DRO_MARGIN = SPACE_LG  # distância até o canto do viewport


class DroOverlay(QFrame):
    """só exibe o que recebe; quem calcula é a janela principal."""

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setObjectName("dro")
        # o overlay não captura o mouse: arrastar por cima dele ainda gira a câmera
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self._axis_values = [self._value_label() for _ in AXES]
        self._feed_value = self._value_label()
        self._process = QLabel()
        self._process.setObjectName("droName")
        self._process.setTextFormat(Qt.TextFormat.RichText)

        grid = QGridLayout(self)
        grid.setContentsMargins(SPACE_LG, SPACE_SM, SPACE_LG, SPACE_SM)
        grid.setHorizontalSpacing(SPACE_SM)
        grid.setVerticalSpacing(SPACE_XXS)
        for row, (axis, value) in enumerate(zip(AXES, self._axis_values)):
            grid.addWidget(self._name_label(axis), row, 0)
            grid.addWidget(value, row, 1)
        grid.setColumnMinimumWidth(2, SPACE_LG)
        grid.addWidget(self._name_label("F"), 0, 3)
        grid.addWidget(self._feed_value, 0, 4)
        grid.addWidget(self._process, 2, 3, 1, 2)

        self.move(DRO_MARGIN, DRO_MARGIN)
        self.hide()

    def show_state(self, position, feed: float, active: bool) -> None:
        """position em mm; feed em mm/min (0 durante uma espera)."""
        for label, value in zip(self._axis_values, position):
            label.setText(f"{value:.3f}")
        self._feed_value.setText(f"{feed:.0f}")
        dot = ACCENT_TEXT if active else TEXT_MUTED
        name = tr("dro_process_on" if active else "dro_process_off")
        self._process.setText(f'<span style="color:{dot}">●</span>&nbsp;{name}')
        self.adjustSize()
        self.show()

    @staticmethod
    def _name_label(text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("droName")
        return label

    @staticmethod
    def _value_label() -> QLabel:
        label = QLabel("0.000")
        label.setObjectName("droValue")
        label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        return label