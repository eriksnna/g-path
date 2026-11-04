"""Ícones da interface: SVGs do Heroicons (Solid), pré-coloridos em duas variantes
(clara/escura) e escolhidos pela variante certa conforme o tema ativo.
"""
from __future__ import annotations

from PySide6.QtGui import QIcon

import config

PLAY = "play"
PAUSE = "pause"
SKIP_BACK = "skip_back"
SKIP_FORWARD = "skip_forward"
REWIND = "rewind"
FAST_FORWARD = "forward"
HELP = "help"
CLOSE = "close"
NEW_FILE = "new_file"
OPEN_FILE = "open_file"
SAVE = "save_file"
DISCARD = "discard"
QUIT = "quit"
APPLY = "apply"
SEARCH = "search"
SETTINGS = "settings"

ICONS_DIR = config.ASSETS_DIR / "icons"


def icon(name: str) -> QIcon:
    path = ICONS_DIR / f"{name}-dark.svg"
    return QIcon(str(path))