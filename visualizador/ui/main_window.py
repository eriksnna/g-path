"""janela principal: liga a interface ao modo de processo, ao modelo e à reprodução."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, QElapsedTimer, QSettings, QTimer, QEasingCurve, QPropertyAnimation
from PySide6.QtGui import QIcon, QCloseEvent, QAction, QKeySequence
from PySide6.QtWidgets import (
    QFileDialog, QFrame, QHBoxLayout, QLabel, QMainWindow, QPushButton,
    QScrollArea, QSplitter, QVBoxLayout, QWidget, QMessageBox, QStackedWidget,
    QLayout, QGraphicsOpacityEffect, QApplication,
)

from config import APP_TITLE, ICON_PATH, TICK_MS, WINDOW_SIZE
from ui.icons import APPLY, DISCARD, NEW_FILE, OPEN_FILE, QUIT, SAVE, SEARCH, SETTINGS, icon

import config
from core.layers import depth_levels
from core.lexer import Issue, clean_line
from core.timeline import TimelineMarks, build_marks, step_layer, step_move
from core.modes import apply_mode, mode_display_name
from core.i18n import tr
from core.parser import parse_gcode
from core.playback import Playback
from core.stats import compute_stats
from core.toolpath import Snapshot, Toolpath
from core.file_safety import UnsafeFileError, check_file_size, check_line_lengths
from core.dialect import dialect_label, get_dialect, process_codes_label, suggest_dialect
from core.file_io import read_gcode_text
from ui.gcode_editor import GCodeEditor
from ui.issues_panel import IssuesPanel
from ui.layer_controls import LayerControls
from ui.mode_controls import ModeControls
from ui.camera_controls import CameraControls
from core.profile_store import load_profiles, save_profiles
from ui.settings_dialog import SettingsDialog
from ui.player_bar import PlayerBar
from ui.stats_panel import StatsPanel
from ui.theme import DARK_QSS
from ui.viewport import ToolpathView
from ui.dro import DroOverlay
from ui.start_panel import StartPanel

def _gcode_filter() -> str:
    patterns = " ".join(f"*{ext}" for ext in config.GCODE_EXTENSIONS)
    return f"G-code ({patterns});;{tr('file_filter_all')} (*)"

def _vsep() -> QFrame:
    """linha vertical fina pra separar grupos de controles na barra superior."""
    line = QFrame()
    line.setFrameShape(QFrame.Shape.VLine)
    line.setFrameShadow(QFrame.Shadow.Plain)
    line.setObjectName("headerSeparator")
    return line

class _ElidingLabel(QLabel):
    def __init__(self, text: str = "", parent=None) -> None:
        super().__init__(parent)
        self._full_text = text
        self.setMinimumWidth(140)
        super().setText(text)

    def setText(self, text: str) -> None:
        self._full_text = text
        self._update_elided_text()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._update_elided_text()

    def _update_elided_text(self) -> None:
        elided = self.fontMetrics().elidedText(
            self._full_text, Qt.TextElideMode.ElideMiddle, self.width()
        )
        super().setText(elided)
        self.setToolTip(self._full_text)

class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.resize(*WINDOW_SIZE)
        self.setWindowIcon(QIcon(str(ICON_PATH)))
        self.setStyleSheet(DARK_QSS)
        self.setAcceptDrops(True) # arrastar e soltar
        self._encoding = "utf-8"

        self._path: Path | None = None
        self._text: str | None = None
        self._saved_text: str | None = None  # último texto gravado em disco (ou None se nunca salvo)
        self._toolpath: Toolpath | None = None
        self._marks = TimelineMarks()
        self._issues: list[Issue] = []
        self._source_lines: list[str] = []
        self._playback = Playback()
        self._profiles, _active_name = load_profiles()
        self._profile = next((p for p in self._profiles if p.name == _active_name), self._profiles[0])

        self._file_label = _ElidingLabel(tr("file_no_file"))
        self._file_label.setObjectName("fileLabel")
        self._profile_label = QLabel()
        self._profile_label.setObjectName("profileLabel")
        self._update_profile_label()
        self._mode_controls = ModeControls()
        self._mode_controls.set_mode(self._profile.mode_key)
        self._editor_toggle = QPushButton(tr("editor_toggle"))
        self._editor_toggle.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._editor_toggle.setObjectName("editorToggle")
        self._editor_toggle.setCheckable(True)
        self._layer_controls = LayerControls()
        self._camera_controls = CameraControls()
        self._viewport = ToolpathView()
        self._dro = DroOverlay(self._viewport)
        self._editor = GCodeEditor()
        self._editor.setVisible(False)
        self._stats_panel = StatsPanel()
        self._issues_panel = IssuesPanel()
        self._player = PlayerBar()

        self._start_panel = StartPanel()
        self._stack = QStackedWidget()

        self._timer = QTimer(self)
        self._timer.setInterval(TICK_MS)
        self._timer.timeout.connect(self._on_tick)
        self._frame_clock = QElapsedTimer()
        self._settings = QSettings(str(config.WINDOW_STATE_FILE), QSettings.Format.IniFormat)

        self._build_layout()
        self._build_menu_bar()
        self.menuBar().setVisible(False)
        self._connect_signals()
        self._player.set_speed(self._playback.speed)
        self._player.set_enabled(False)
        self._layer_controls.set_levels([])
        self._restore_window_state()
        self._viewport.setFocus()

    # --- montagem ---

    def _build_layout(self) -> None:
        central = QWidget()
        central.setObjectName("central")
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)

        header = QHBoxLayout()
        header.setSpacing(10)
        header.addWidget(self._file_label, 1)
        header.addWidget(self._profile_label)
        header.addWidget(_vsep())
        header.addWidget(self._mode_controls)
        header.addWidget(self._layer_controls)
        header.addWidget(_vsep())
        header.addWidget(self._editor_toggle)
        header.addWidget(self._camera_controls)

        stats_scroll = QScrollArea()
        stats_scroll.setWidgetResizable(True)
        stats_scroll.setFrameShape(QFrame.Shape.NoFrame)
        stats_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        stats_scroll.setWidget(self._stats_panel)

        side = QSplitter(Qt.Orientation.Vertical)
        side.addWidget(stats_scroll)
        side.addWidget(self._issues_panel)
        side.setStretchFactor(0, 1)
        side.setStretchFactor(1, 1)
        side.setChildrenCollapsible(True)

        side.setSizes([420, 220])
        self._issues_panel.setMinimumHeight(160)

        self._viewport.setMinimumSize(280, 180)
        main_area = QSplitter(Qt.Orientation.Vertical)
        main_area.addWidget(self._viewport)
        main_area.addWidget(self._editor)
        main_area.setStretchFactor(0, 1)
        main_area.setStretchFactor(1, 0)
        main_area.setChildrenCollapsible(True)

        body = QSplitter(Qt.Orientation.Horizontal)
        body.addWidget(main_area)
        body.addWidget(side)
        body.setStretchFactor(0, 1)
        body.setSizes([760, 320])
        body.setChildrenCollapsible(True)

        self._header_widget = QWidget()
        self._header_widget.setLayout(header)
        self._header_widget.setVisible(False)
        self._player.setVisible(False)

        workspace = QWidget()
        workspace_layout = QVBoxLayout(workspace)
        workspace_layout.setContentsMargins(12, 12, 12, 12)
        workspace_layout.setSpacing(10)
        workspace_layout.addWidget(self._header_widget)
        workspace_layout.addWidget(body, 1)
        workspace_layout.addWidget(self._player)

        self._stack.addWidget(self._start_panel)
        self._stack.addWidget(workspace)
        self._stack.setCurrentWidget(self._start_panel)

        root.addWidget(self._stack, 1)
        self.setCentralWidget(central)

    def _build_menu_bar(self) -> None:
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu(tr("menu_file"))

        new_action = QAction(tr("menu_new"), self)
        new_action.setIcon(icon(NEW_FILE))
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self._start_blank)
        file_menu.addAction(new_action)

        open_action = QAction(tr("menu_open"), self)
        open_action.setIcon(icon(OPEN_FILE))
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(lambda: self.open_file())
        file_menu.addAction(open_action)
        self._recent_menu = file_menu.addMenu(tr("menu_open_recent"))
        self._recent_menu.aboutToShow.connect(self._refresh_recent_menu)

        file_menu.addSeparator()

        save_action = QAction(tr("menu_save"), self)
        save_action.setIcon(icon(SAVE))
        save_action.triggered.connect(lambda: self._save_edited_text(self._editor.text()))
        file_menu.addAction(save_action)
        save_action.setShortcut(QKeySequence.StandardKey.Save)

        save_as_action = QAction(tr("menu_save_as"), self)
        save_as_action.setIcon(icon(SAVE))
        save_as_action.triggered.connect(lambda: self._save_edited_text_as(self._editor.text()))
        file_menu.addAction(save_as_action)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)

        file_menu.addSeparator()

        close_project_action = QAction(tr("menu_close_project"), self)
        close_project_action.setIcon(icon(DISCARD))
        close_project_action.triggered.connect(self._reset_to_start)
        file_menu.addAction(close_project_action)

        file_menu.addSeparator()

        quit_action = QAction(tr("menu_quit"), self)
        quit_action.setIcon(icon(QUIT))
        quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        edit_menu = menu_bar.addMenu(tr("menu_edit"))

        apply_action = QAction(tr("menu_apply_changes"), self)
        apply_action.setIcon(icon(APPLY))
        apply_action.triggered.connect(lambda: self._apply_edited_text(self._editor.text()))
        edit_menu.addAction(apply_action)

        comment_action = QAction(tr("menu_toggle_comment"), self)
        comment_action.triggered.connect(self._editor.toggle_comment)
        edit_menu.addAction(comment_action)

        find_action = QAction(tr("menu_find"), self)
        find_action.setIcon(icon(SEARCH))
        find_action.triggered.connect(self._show_editor_find)
        edit_menu.addAction(find_action)

        settings_menu = menu_bar.addMenu(tr("menu_settings"))

        settings_action = QAction(tr("menu_settings_open"), self)
        settings_action.setIcon(icon(SETTINGS))
        settings_action.triggered.connect(self._open_settings)
        settings_menu.addAction(settings_action)

    def _reset_to_start(self) -> None:
        """fecha o projeto atual e volta à tela inicial, esquecendo o último arquivo lembrado."""
        if not self._confirm_discard_changes():
            return
        self._path = None
        self._text = None
        self._saved_text = None
        self._settings.remove("window/last_file")
        self._file_label.setText(tr("file_no_file"))
        self._editor.set_text("")
        self._show_empty()
        self._header_widget.setVisible(False)
        self._player.setVisible(False)
        self.menuBar().setVisible(False)
        self._stack.setCurrentIndex(0)
        self._fade_in_current_page()

    def _enter_workspace(self) -> None:
        """sai da tela inicial: mostra cabeçalho, área de trabalho e barra de reprodução."""
        self._header_widget.setVisible(True)
        self._player.setVisible(True)
        self.menuBar().setVisible(True)
        self._stack.setCurrentIndex(1)
        self._fade_in_current_page()

    def _fade_in_current_page(self) -> None:
        page = self._stack.currentWidget()
        effect = QGraphicsOpacityEffect(page)
        page.setGraphicsEffect(effect)
        animation = QPropertyAnimation(effect, b"opacity", self)
        animation.setDuration(180)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        animation.finished.connect(lambda: page.setGraphicsEffect(None))
        animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
        self._page_fade = animation  # mantém viva até terminar

    def _restore_window_state(self) -> None:
        """restaura a geometria da janela e reabre o último arquivo, se ele ainda existir."""
        geometry = self._settings.value("window/geometry")
        if geometry is not None:
            self.restoreGeometry(geometry)
        last_file = self._settings.value("window/last_file")
        if last_file:
            path = Path(str(last_file))
            if path.exists():
                self.load_file(path)

    def _connect_signals(self) -> None:
        self._mode_controls.changed.connect(self._on_mode_changed)
        self._editor_toggle.toggled.connect(self._on_editor_toggled)    
        self._editor.save_requested.connect(self._save_edited_text)
        self._editor.save_as_requested.connect(self._save_edited_text_as)
        self._editor.apply_requested.connect(self._apply_edited_text)
        self._camera_controls.view_requested.connect(self._viewport.set_preset_view)

        p = self._player
        p.play_clicked.connect(self._toggle_play)
        p.start_clicked.connect(self._go_to_start)
        p.end_clicked.connect(self._go_to_end)
        p.step_clicked.connect(self._step)
        p.scrub_started.connect(self._pause)
        p.scrubbed.connect(self._scrub_to)
        p.speed_changed.connect(self._change_speed)

        c = self._layer_controls
        c.filter_changed.connect(self._viewport.set_layer_filter)
        c.depth_coloring_toggled.connect(self._viewport.set_depth_coloring)

        self._issues_panel.issue_selected.connect(self._go_to_issue)
        self._issues_panel.issue_selected.connect(self._editor.goto_line)
        self._issues_panel.dialect_requested.connect(self._use_dialect)

        self._start_panel.open_requested.connect(lambda: self.open_file())
        self._start_panel.blank_requested.connect(self._start_blank)

        self._editor_status_timer = QTimer(self)
        self._editor_status_timer.setInterval(300)
        self._editor_status_timer.timeout.connect(self._update_title)
        self._editor_status_timer.start()

    # --- carregamento ---

    def open_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, tr("dialog_open_title"), "", _gcode_filter())
        if path:
            self.load_file(Path(path))

    def _open_settings(self) -> None:
        """abre a tela de ajustes (perfis: modo, dialeto e limites)."""
        dialog = SettingsDialog(self, profiles=self._profiles, active_profile=self._profile)
        dialog.exec()
        self._profiles = dialog.profiles()
        self._profile = dialog.current_profile()
        save_profiles(self._profiles, self._profile.name)
        self._mode_controls.set_mode(self._profile.mode_key)
        self._update_profile_label()
        self._reload()

    def _update_profile_label(self) -> None:
        name = tr("profile_label").format(name=self._profile.name)
        self._profile_label.setText(f"{name}  ·  {dialect_label(self._profile.dialect_key)}")
        self._profile_label.setToolTip(tr("profile_dialect_tooltip").format(
            codes=process_codes_label(self._profile.dialect_key)))

    def _update_dialect_suggestion(self) -> None:
        key = suggest_dialect(self._text or "", self._profile.dialect_key)
        if key is None:
            self._issues_panel.show_dialect_suggestion(None)
            return
        self._issues_panel.show_dialect_suggestion(
            key,
            tr("dialect_suggestion").format(
                codes=process_codes_label(key), current=dialect_label(self._profile.dialect_key)),
            tr("dialect_suggestion_action").format(name=dialect_label(key)),
        )

    def _use_dialect(self, key: str) -> None:
        """troca o dialeto do perfil ativo pelo sugerido e reinterpreta o programa."""
        self._profile.dialect_key = key
        save_profiles(self._profiles, self._profile.name)
        self._update_profile_label()
        self._reload()

    def _on_mode_changed(self) -> None:
        """o usuário trocou o modo (ou um parâmetro de cordão) na tela principal."""
        mode = self._mode_controls.current_mode()
        self._profile.mode_key = mode.key
        save_profiles(self._profiles, self._profile.name)
        self._reload()

    def _start_blank(self) -> None:
        """começa um programa vazio direto no editor, sem arquivo de origem."""
        if not self._confirm_discard_changes():
            return
        self._path = None
        self._settings.remove("window/last_file")
        self._text = ""
        self._saved_text = ""
        self._file_label.setText(tr("file_new_unsaved"))
        self._editor.set_text("")
        self._editor_toggle.setChecked(True)
        self._enter_workspace()
        self._show_empty(status=tr("status_program_new"))
        self._encoding = "utf-8"

    def _recent_files(self) -> list[str]:
        value = self._settings.value("window/recent_files", [])
        if isinstance(value, str):  # QSettings devolve string quando sobra só 1 item salvo
            value = [value]
        return list(value or [])

    def _add_recent_file(self, path: Path) -> None:
        recent = [p for p in self._recent_files() if p != str(path)]
        recent.insert(0, str(path))
        self._settings.setValue("window/recent_files", recent[:config.MAX_RECENT_FILES])

    def _refresh_recent_menu(self) -> None:
        self._recent_menu.clear()
        recent = [p for p in self._recent_files() if Path(p).exists()]
        if not recent:
            empty_action = QAction(tr("menu_recent_empty"), self)
            empty_action.setEnabled(False)
            self._recent_menu.addAction(empty_action)
            return
        for path_str in recent:
            action = QAction(path_str, self)
            action.triggered.connect(lambda checked=False, p=path_str: self.load_file(Path(p)))
            self._recent_menu.addAction(action)

    def load_file(self, path: Path) -> None:
        if not self._confirm_discard_changes():
            return
        try:
            check_file_size(path)
            text, encoding = read_gcode_text(path)
            check_line_lengths(text)
        except UnsafeFileError as err:
            self._show_open_error(tr("status_file_rejected").format(err=err))
            return
        except OSError as err:
            self._show_open_error(tr("status_open_error").format(err=err))
            return
        self._encoding = encoding
        self._path = path
        self._text = text
        self._saved_text = text
        self._file_label.setText(str(path))
        self._settings.setValue("window/last_file", str(path))
        self._add_recent_file(path)
        self._editor.set_text(text)
        self._enter_workspace()
        self._reload()

    def _show_open_error(self, message: str) -> None:
        """na tela inicial a barra de status está oculta, então o erro vai num diálogo."""
        self._player.set_status(message)
        QMessageBox.warning(self, tr("open_error_title"), message)

    def _confirm_discard_changes(self) -> bool:
        """pergunta antes de descartar edições não salvas. True se pode prosseguir."""
        if not self._has_unsaved_changes():
            return True
        answer = QMessageBox.question(
            self, tr("confirm_discard_title"),
            tr("confirm_discard_text"),
            QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel,
        )
        return answer == QMessageBox.StandardButton.Discard

    def _apply_edited_text(self, text: str) -> None:
        """o usuário editou o G-code no painel e pediu para reinterpretar."""
        self._text = text
        self._editor.mark_applied()
        self._reload()

    def _save_edited_text(self, text: str) -> None:
        """salva no arquivo aberto; sem arquivo de origem, pede um caminho novo."""
        if self._path is None:
            self._save_edited_text_as(text)
            return
        self._write_to_path(self._path, text)

    def _save_edited_text_as(self, text: str) -> None:
        """sempre pergunta o caminho, mesmo que já exista um arquivo aberto."""
        path_str, _ = QFileDialog.getSaveFileName(self, tr("dialog_save_title"), "", _gcode_filter())
        if not path_str:
            return
        path = Path(path_str)
        if self._write_to_path(path, text):
            self._path = path
            self._file_label.setText(str(path))

    def _write_to_path(self, path: Path, text: str) -> bool:
        try:
            try:
                path.write_text(text, encoding=self._encoding)
            except UnicodeEncodeError:
                # texto novo tem caractere que a codificação antiga não comporta
                self._encoding = "utf-8"
                path.write_text(text, encoding=self._encoding)
        except OSError as err:
            QMessageBox.warning(self, tr("save_error_title"), tr("save_error_text").format(err=err))
            return False
        self._apply_edited_text(text)
        self._saved_text = text
        self._player.set_status(tr("status_saved_at").format(path=path))
        return True

    def _has_unsaved_changes(self) -> bool:
        if self._text is None:
            return False
        if self._editor.is_modified():
            return True
        return self._text != self._saved_text

    def _update_title(self) -> None:
        mark = "* " if self._has_unsaved_changes() else ""
        self.setWindowTitle(f"{mark}{APP_TITLE}")

    def _reload(self) -> None:
        """reinterpreta o texto atual com o modo e o dialeto escolhidos."""
        if self._text is None:
            return
        self._pause()

        mode = self._mode_controls.current_mode()
        dialect = get_dialect(self._profile.dialect_key)
        limits = self._profile.limits
        result = parse_gcode(
            self._text, default_feed=self._profile.default_feed,
            dialect=dialect, limits=limits, arc_step_deg=self._profile.arc_step_deg,
        )
        moves = apply_mode(result.moves, mode)

        self._source_lines = self._text.splitlines()
        self._issues = sorted([*result.issues, *mode.validate(moves)], key=lambda i: i.line)
        self._issues_panel.show_issues(self._issues)
        self._update_dialect_suggestion()
        self._layer_controls.setVisible(mode.key != "deposicao")

        if not moves:
            status = (tr("status_no_moves_see_issues").format(count=len(self._issues))
                      if self._issues else None)
            self._show_empty(status=status, clear_issues=False)
            return

        toolpath = Toolpath(moves, rapid_feed=self._profile.rapid_feed, min_feed=self._profile.min_feed)
        levels = depth_levels(toolpath)
        self._toolpath = toolpath
        self._layer_controls.set_levels(levels)
        self._playback.reset(toolpath.total_time)
        self._viewport.show_toolpath(toolpath, levels)
        self._viewport.set_show_torch(mode.key == "deposicao")
        self._stats_panel.show_program(compute_stats(toolpath, result.commands))
        self._stats_panel.show_mode(mode_display_name(mode.key), mode.cards(toolpath))
        self._player.set_enabled(True)
        self._marks = build_marks(toolpath, levels, self._issues)
        self._player.set_enabled(True)
        self._player.set_marks(self._marks)
        self._player.set_status("")
        self._refresh()

    def _show_empty(self, status: str | None = None, clear_issues: bool = True) -> None:
        status = status if status is not None else tr("status_no_moves")
        self._toolpath = None
        self._viewport.clear()
        self._dro.hide()
        self._stats_panel.clear()
        self._layer_controls.set_levels([])
        if clear_issues:
            self._issues = []
            self._issues_panel.show_issues(self._issues)
            self._issues_panel.show_dialect_suggestion(None)
        self._player.set_enabled(False)
        self._player.set_status(status, timeout_ms=0)
        self._editor.set_running_line(None)

    # --- validação ---

    def _go_to_issue(self, line: int) -> None:
        self._editor_toggle.setChecked(True)
        if 1 <= line <= len(self._source_lines):
            self._issues_panel.show_source(line, self._source_lines[line - 1].strip())

        if self._toolpath is None:
            return
        t = self._toolpath.time_at_line(line)
        if t is None:
            self._player.set_status(tr("status_no_moves_from_line").format(line=line))
            return

        self._playback.pause()
        self._playback.seek(t)
        self._refresh()

    # --- ações de reprodução ---

    def _toggle_play(self) -> None:
        self._playback.toggle()
        self._refresh()

    def _pause(self) -> None:
        self._playback.pause()
        self._timer.stop()
        self._refresh()

    def _go_to_start(self) -> None:
        self._playback.pause()
        self._playback.seek(0.0)
        self._refresh()

    def _go_to_end(self) -> None:
        self._playback.pause()
        self._playback.seek(self._playback.total_time)
        self._refresh()

    def _step(self, direction: int) -> None:
        """pula um movimento; com Shift, uma camada inteira."""
        if self._toolpath is None:
            return
        t = self._playback.elapsed
        by_layer = QApplication.keyboardModifiers() & Qt.KeyboardModifier.ShiftModifier
        if by_layer and self._marks.layer_starts.size:
            target = step_layer(self._marks, t, direction)
        else:
            target = step_move(self._toolpath, t, direction)
        self._playback.pause()
        self._playback.seek(target)
        self._refresh()

    def _scrub_to(self, fraction: float) -> None:
        self._playback.seek_fraction(fraction)
        self._refresh()

    def _change_speed(self, value: float) -> None:
        self._playback.set_speed(value)
        self._player.set_speed(self._playback.speed)
        self._refresh()

    def _on_tick(self) -> None:
        seconds = self._frame_clock.restart() / 1000.0
        self._playback.advance(seconds)
        self._refresh()

    # --- sincronização da tela com o estado ---

    def _refresh(self) -> None:
        if self._toolpath is None:
            return

        pb = self._playback
        snapshot = self._toolpath.snapshot(pb.elapsed)
        self._viewport.render(snapshot)
        self._player.set_progress(pb.progress, pb.elapsed)
        self._player.set_playing(pb.playing)
        self._update_position_chips(snapshot)
        index = min(snapshot.done, self._toolpath.count - 1)
        self._dro.show_state(snapshot.head, float(self._toolpath.feeds[index]), snapshot.active)
        self._stats_panel.show_progress(
            pb.elapsed, pb.total_time, snapshot.done, self._toolpath.count,
        )
        self._update_running_line(snapshot)
        self._sync_timer()

    def _update_running_line(self, snapshot: Snapshot) -> None:
        """destaca no editor a linha de origem do movimento atualmente em execução."""
        if not self._editor.isVisible():
            return
        if self._toolpath is None or self._toolpath.count == 0:
            self._editor.set_running_line(None)
            return
        index = min(max(snapshot.done, 0), self._toolpath.count - 1)
        self._editor.set_running_line(int(self._toolpath.lines[index]))

    def _update_position_chips(self, snapshot: Snapshot) -> None:
        index = min(snapshot.done, self._toolpath.count - 1)
        line = int(self._toolpath.lines[index])
        raw = self._source_lines[line - 1] if 1 <= line <= len(self._source_lines) else ""
        self._player.set_position(
            line, clean_line(raw) or raw.strip(),
            self._marks.layer_at(self._playback.elapsed), len(self._marks.layer_starts),
            snapshot.active,
        )

    def _sync_timer(self) -> None:
        if self._playback.playing and not self._timer.isActive():
            self._frame_clock.start()
            self._timer.start()
        elif not self._playback.playing and self._timer.isActive():
            self._timer.stop()
    
    def closeEvent(self, event: QCloseEvent) -> None:
        if self._has_unsaved_changes() and not self._confirm_discard_changes():
            event.ignore()
            return
        self._settings.setValue("window/geometry", self.saveGeometry())
        event.accept()

    def keyPressEvent(self, event) -> None:
        """atalhos de reprodução. só chegam aqui quando o editor não está com o foco."""
        actions = {
            Qt.Key.Key_Space: self._toggle_play,
            Qt.Key.Key_Left: lambda: self._step(-1),
            Qt.Key.Key_Right: lambda: self._step(1),
            Qt.Key.Key_Home: self._go_to_start,
            Qt.Key.Key_End: self._go_to_end,
        }
        action = actions.get(event.key())
        if action is None or self._toolpath is None:
            super().keyPressEvent(event)
            return
        action()
        event.accept()

    def dropEvent(self, event) -> None:
        path = self._dropped_gcode_path(event.mimeData())
        if path is not None:
            self.load_file(path)
            event.acceptProposedAction()

    @staticmethod
    def _dropped_gcode_path(mime) -> Path | None:
        if not mime.hasUrls():
            return None
        for url in mime.urls():
            if url.isLocalFile() and Path(url.toLocalFile()).suffix.lower() in config.GCODE_EXTENSIONS:
                return Path(url.toLocalFile())
        return None

    def _show_editor_find(self) -> None:
        self._editor_toggle.setChecked(True)
        self._editor.show_find()

    def _on_editor_toggled(self, visible: bool) -> None:
        self._editor.setVisible(visible)
        self._player.set_chips_allowed(not visible)
        if visible and self._toolpath is not None:
            self._update_running_line(self._toolpath.snapshot(self._playback.elapsed))