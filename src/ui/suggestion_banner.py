"""faixa de sugestão acima da área de trabalho: uma frase, uma ação e um botão de fechar."""
from __future__ import annotations

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton

from ui.icons import CLOSE, icon
from ui.theme import SPACE_LG, SPACE_SM, SPACE_XS


class SuggestionBanner(QFrame):
    accepted = Signal(str)   # chave da sugestão aceita
    dismissed = Signal(str)  # chave da sugestão dispensada

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("suggestion")
        self._key = ""

        self._text = QLabel()
        self._text.setObjectName("suggestionText")
        self._action = QPushButton()
        self._action.setObjectName("suggestionButton")
        self._action.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._action.clicked.connect(lambda: self.accepted.emit(self._key))
        close = QPushButton()
        close.setObjectName("suggestionClose")
        close.setIcon(icon(CLOSE))
        close.setIconSize(QSize(12, 12))
        close.setFixedSize(22, 22)
        close.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        close.clicked.connect(self._dismiss)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(SPACE_LG, SPACE_XS, SPACE_SM, SPACE_XS)
        layout.setSpacing(SPACE_LG)
        layout.addWidget(self._text)
        layout.addWidget(self._action)
        layout.addStretch()
        layout.addWidget(close)
        self.hide()

    def show_suggestion(self, key: str, text: str, action: str) -> None:
        self._key = key
        self._text.setText(text)
        self._action.setText(action)
        self.show()

    def _dismiss(self) -> None:
        self.hide()
        self.dismissed.emit(self._key)