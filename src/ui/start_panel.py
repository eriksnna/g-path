"""tela inicial: abrir um arquivo G-code existente, um recente, ou começar do zero."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

import config
from core.i18n import tr
from ui.icons import SETTINGS, icon
from ui.start_background import StartBackground
from ui.text import plain_tooltip
from ui.theme import SPACE_LG, SPACE_MD, SPACE_SM, SPACE_XL, SPACE_XXL, SPACE_XXS, TEXT_SECONDARY

TITLE = "G-Path"
LOGO_SIZE = 56
CONTENT_WIDTH = 340
BUTTON_HEIGHT = 38
RECENT_ROW_HEIGHT = 32
MAX_RECENT_SHOWN = 5
SETTINGS_BUTTON_SIZE = 32
FOLDER_MAX_WIDTH = 170  # pastas mais longas são abreviadas no meio


class _RecentRow(QPushButton):
    """linha clicável: nome do arquivo em destaque e a pasta, discreta, à direita."""

    def __init__(self, path: str) -> None:
        super().__init__()
        self.setObjectName("recentRow")
        self.setFixedHeight(RECENT_ROW_HEIGHT)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(plain_tooltip(path))

        name = QLabel(Path(path).name)
        name.setObjectName("recentName")
        folder = QLabel()
        folder.setObjectName("recentFolder")
        folder.setText(folder.fontMetrics().elidedText(
            str(Path(path).parent), Qt.TextElideMode.ElideMiddle, FOLDER_MAX_WIDTH))
        for label in (name, folder):
            label.setTextFormat(Qt.TextFormat.PlainText)
            # o clique passa pelos rótulos e chega ao botão
            label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(SPACE_MD, 0, SPACE_MD, 0)
        layout.setSpacing(SPACE_LG)
        layout.addWidget(name)
        layout.addStretch()
        layout.addWidget(folder)


class StartPanel(QFrame):
    open_requested = Signal()
    blank_requested = Signal()
    recent_requested = Signal(str)  # caminho do arquivo
    settings_requested = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("startPanel")

        self._background = StartBackground(self)

        logo = QLabel()
        logo.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        logo.setPixmap(QPixmap(str(config.ASSETS_DIR / "logo.png")).scaled(
            LOGO_SIZE, LOGO_SIZE,
            Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation,
        ))
        title = QLabel(TITLE)
        title.setObjectName("startTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self._subtitle = QLabel(tr("start_subtitle"))
        self._subtitle.setObjectName("startSubtitle")
        self._subtitle.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self._subtitle.setWordWrap(True)
        self._subtitle.setFixedWidth(CONTENT_WIDTH)

        open_button = QPushButton(tr("start_open_file"))
        open_button.setObjectName("startButton")
        open_button.setFixedHeight(BUTTON_HEIGHT)
        open_button.clicked.connect(self.open_requested.emit)
        blank_button = QPushButton(tr("start_blank"))
        blank_button.setObjectName("startButtonSecondary")
        blank_button.setFixedHeight(BUTTON_HEIGHT)
        blank_button.clicked.connect(self.blank_requested.emit)
        buttons = QHBoxLayout()
        buttons.setSpacing(SPACE_SM)
        buttons.addWidget(open_button, 1)
        buttons.addWidget(blank_button, 1)

        drop_hint = QLabel(tr("start_drop_hint"))
        drop_hint.setObjectName("startHint")
        drop_hint.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self._recent_title = QLabel(tr("start_recent_title").upper())
        self._recent_title.setObjectName("sectionTitle")
        self._recent_list = QVBoxLayout()
        self._recent_list.setSpacing(SPACE_XXS)
        self._recent_title.hide()

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(SPACE_SM)
        content_layout.addWidget(logo)
        content_layout.addWidget(title)
        content_layout.addWidget(self._subtitle)
        content_layout.addSpacing(SPACE_XXL)
        content_layout.addLayout(buttons)
        content_layout.addWidget(drop_hint)
        content_layout.addSpacing(SPACE_XXL)
        content_layout.addWidget(self._recent_title)
        content_layout.addLayout(self._recent_list)
        content = QWidget()
        content.setFixedWidth(CONTENT_WIDTH)
        content.setLayout(content_layout)

        settings_button = QPushButton()
        settings_button.setObjectName("startSettings")
        settings_button.setIcon(icon(SETTINGS, TEXT_SECONDARY))
        settings_button.setIconSize(QSize(18, 18))
        settings_button.setFixedSize(SETTINGS_BUTTON_SIZE, SETTINGS_BUTTON_SIZE)
        settings_button.setToolTip(tr("settings_title"))
        settings_button.clicked.connect(self.settings_requested.emit)
        top = QHBoxLayout()
        top.addStretch()
        top.addWidget(settings_button)

        footer = QLabel(f"erik senna ©2026  ·  v{config.APP_VERSION}")
        footer.setObjectName("startFooter")
        footer.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(SPACE_XL, SPACE_XL, SPACE_XL, SPACE_XXL)
        outer.addLayout(top)
        outer.addStretch(1)
        outer.addWidget(content, 0, Qt.AlignmentFlag.AlignHCenter)
        outer.addStretch(2)  # conteúdo no terço de cima; a cena animada fica livre embaixo
        outer.addWidget(footer)
        self._background.lower()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        # texto com quebra de linha: sem a altura real, o layout reserva só uma linha
        # e as últimas linhas da lista de recentes saem cortadas
        self._subtitle.setFixedHeight(self._subtitle.heightForWidth(CONTENT_WIDTH))

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._background.setGeometry(self.rect())

    def set_recent(self, paths: list[str]) -> None:
        """mostra até MAX_RECENT_SHOWN arquivos recentes; sem nenhum, a seção some."""
        while self._recent_list.count():
            self._recent_list.takeAt(0).widget().deleteLater()
        for path in paths[:MAX_RECENT_SHOWN]:
            row = _RecentRow(path)
            row.clicked.connect(lambda _checked=False, p=path: self.recent_requested.emit(p))
            self._recent_list.addWidget(row)
        self._recent_title.setVisible(bool(paths))