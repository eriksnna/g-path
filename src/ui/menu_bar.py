"""barra de menus da janela principal. só monta os menus; o que cada item faz vem de fora."""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QMenu

from core.i18n import tr
from ui.icons import APPLY, DISCARD, NEW_FILE, OPEN_FILE, QUIT, SAVE, SEARCH, SETTINGS, icon


@dataclass(frozen=True)
class MenuHandlers:
    new: Callable[[], None]
    open: Callable[[], None]
    open_recent: Callable[[Path], None]
    recent_files: Callable[[], list[str]]
    save: Callable[[], None]
    save_as: Callable[[], None]
    close_project: Callable[[], None]
    quit: Callable[[], None]
    apply: Callable[[], None]
    toggle_comment: Callable[[], None]
    find: Callable[[], None]
    settings: Callable[[], None]


def build_menu_bar(window: QMainWindow, handlers: MenuHandlers) -> None:
    menu_bar = window.menuBar()

    file_menu = menu_bar.addMenu(tr("menu_file"))
    _add(window, file_menu, "menu_new", handlers.new, NEW_FILE, QKeySequence.StandardKey.New)
    _add(window, file_menu, "menu_open", handlers.open, OPEN_FILE, QKeySequence.StandardKey.Open)
    recent_menu = file_menu.addMenu(tr("menu_open_recent"))
    recent_menu.aboutToShow.connect(lambda: _fill_recent(window, recent_menu, handlers))
    file_menu.addSeparator()
    _add(window, file_menu, "menu_save", handlers.save, SAVE, QKeySequence.StandardKey.Save)
    _add(window, file_menu, "menu_save_as", handlers.save_as, SAVE, QKeySequence.StandardKey.SaveAs)
    file_menu.addSeparator()
    _add(window, file_menu, "menu_close_project", handlers.close_project, DISCARD)
    file_menu.addSeparator()
    _add(window, file_menu, "menu_quit", handlers.quit, QUIT, QKeySequence.StandardKey.Quit)

    edit_menu = menu_bar.addMenu(tr("menu_edit"))
    _add(window, edit_menu, "menu_apply_changes", handlers.apply, APPLY)
    _add(window, edit_menu, "menu_toggle_comment", handlers.toggle_comment)
    _add(window, edit_menu, "menu_find", handlers.find, SEARCH)

    settings_menu = menu_bar.addMenu(tr("menu_settings"))
    _add(window, settings_menu, "menu_settings_open", handlers.settings, SETTINGS)


def _add(window: QMainWindow, menu: QMenu, text_key: str, handler: Callable[[], None],
         icon_name: str | None = None, shortcut: QKeySequence.StandardKey | None = None) -> QAction:
    # a ação pertence à janela, como antes: é o que mantém os atalhos valendo na janela toda
    action = QAction(tr(text_key), window)
    if icon_name is not None:
        action.setIcon(icon(icon_name))
    if shortcut is not None:
        action.setShortcut(shortcut)
    action.triggered.connect(lambda _checked=False: handler())
    menu.addAction(action)
    return action


def _fill_recent(window: QMainWindow, menu: QMenu, handlers: MenuHandlers) -> None:
    """remonta a lista a cada abertura do submenu, para refletir arquivos movidos ou apagados."""
    menu.clear()
    recent = handlers.recent_files()
    if not recent:
        empty = QAction(tr("menu_recent_empty"), window)
        empty.setEnabled(False)
        menu.addAction(empty)
        return
    for path_str in recent:
        action = QAction(path_str, window)
        action.triggered.connect(lambda _checked=False, p=path_str: handlers.open_recent(Path(p)))
        menu.addAction(action)