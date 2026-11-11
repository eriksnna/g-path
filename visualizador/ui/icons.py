"""Ícones da interface: Phosphor Icons (MIT), um SVG por ícone em assets/icons/.

O SVG é desenhado e depois tingido na cor pedida, então a cor original do
arquivo não importa e não é preciso manter versões clara/escura separadas.
"""
from __future__ import annotations

from functools import lru_cache

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

import config
from ui.theme import TEXT_MUTED, TEXT_PRIMARY

# player (fill só no play/pause, para eles terem mais peso que o resto)
PLAY = "play-fill"
PAUSE = "pause-fill"
SKIP_BACK = "skip-back"
SKIP_FORWARD = "skip-forward"
REWIND = "rewind"
FAST_FORWARD = "fast-forward"

# menus e editor
NEW_FILE = "file-plus"
OPEN_FILE = "folder-open"
SAVE = "floppy-disk"
DISCARD = "x-square"
QUIT = "sign-out"
APPLY = "check"
SEARCH = "magnifying-glass"
SETTINGS = "gear-six"
HELP = "question"
CLOSE = "x"

ICONS_DIR = config.ASSETS_DIR / "icons"
RENDER_SIZE = 64  # desenha grande e deixa o Qt reduzir; fica nítido em telas HiDPI


def _tinted(name: str, color: str) -> QPixmap:
    pixmap = QPixmap(RENDER_SIZE, RENDER_SIZE)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    QSvgRenderer(str(ICONS_DIR / f"{name}.svg")).render(painter, QRectF(0, 0, RENDER_SIZE, RENDER_SIZE))
    # SourceIn mantém só a forma do desenho e troca a cor
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), QColor(color))
    painter.end()
    return pixmap


@lru_cache(maxsize=None)
def icon(name: str, color: str = TEXT_PRIMARY) -> QIcon:
    result = QIcon()
    result.addPixmap(_tinted(name, color), QIcon.Mode.Normal)
    result.addPixmap(_tinted(name, TEXT_MUTED), QIcon.Mode.Disabled)
    return result