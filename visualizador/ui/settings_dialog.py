"""Tela de Ajustes: navegação lateral com seções (Perfis, Atalhos, ...).

Cada perfil reúne modo de processo, dialeto e limites de curso: a configuração
completa de uma máquina.
"""
from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QListWidget,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

import json

import config
from core.dialect import dialect_choices
from core.machine_profile import MachineProfile, default_profiles
from core.modes import mode_choices
from core.i18n import LANGUAGES, get_language, set_language, tr

def _shortcuts_text() -> str:
    return (
        "Ctrl+F           {find}\n"
        "Ctrl+Return      {apply}\n"
        "Ctrl+/           {comment}\n"
        "Ctrl+S           {save}\n"
        "Ctrl+Shift+S     {save_as}\n"
    ).format(
        find=tr("editor_shortcut_find"),
        apply=tr("editor_shortcut_apply"),
        comment=tr("editor_shortcut_comment"),
        save=tr("editor_shortcut_save"),
        save_as=tr("editor_shortcut_save_as"),
    )


class _ProfilesPage(QWidget):
    """Lista de perfis: cada perfil reúne modo, dialeto e limites de curso."""

    changed = Signal()

    def __init__(
        self,
        profiles: list[MachineProfile] | None = None,
        active_profile: MachineProfile | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._profiles: list[MachineProfile] = list(profiles) if profiles else default_profiles()
        self._active: MachineProfile = active_profile or self._profiles[0]
        self._spinboxes: dict[str, tuple[QDoubleSpinBox, QDoubleSpinBox]] = {}
        self._loading = False

        layout = QVBoxLayout(self)

        self._profile_combo = QComboBox()
        for profile in self._profiles:
            self._profile_combo.addItem(profile.name)
        start_row = self._profiles.index(self._active) if self._active in self._profiles else 0
        self._profile_combo.setCurrentIndex(start_row)
        self._profile_combo.currentIndexChanged.connect(self._on_profile_selected)
        layout.addWidget(QLabel(tr("profile_combo_label")))
        layout.addWidget(self._profile_combo)

        profile_buttons = QHBoxLayout()
        add_button = QPushButton(tr("btn_save_as_profile"))
        add_button.clicked.connect(self._add_profile)
        remove_button = QPushButton(tr("btn_remove_profile"))
        remove_button.clicked.connect(self._remove_profile)
        profile_buttons.addWidget(add_button)
        profile_buttons.addWidget(remove_button)
        layout.addLayout(profile_buttons)

        config_box = QGroupBox(tr("group_profile_config"))
        form = QFormLayout(config_box)

        self._mode_combo = QComboBox()
        for label, key in mode_choices():
            self._mode_combo.addItem(label, key)
        self._mode_combo.currentIndexChanged.connect(self._on_fields_edited)
        form.addRow(tr("label_mode_colon"), self._mode_combo)

        self._dialect_combo = QComboBox()
        for label, key in dialect_choices():
            self._dialect_combo.addItem(label, key)
        self._dialect_combo.currentIndexChanged.connect(self._on_fields_edited)
        form.addRow(tr("label_dialect_colon"), self._dialect_combo)

        layout.addWidget(config_box)

        limits_box = QGroupBox(tr("group_travel_limits"))
        limits_form = QFormLayout(limits_box)
        for axis in ("X", "Y", "Z"):
            lo = QDoubleSpinBox()
            hi = QDoubleSpinBox()
            for spin in (lo, hi):
                spin.setRange(-1_000_000.0, 1_000_000.0)
                spin.setDecimals(2)
                spin.valueChanged.connect(self._on_fields_edited)
            row = QHBoxLayout()
            row.addWidget(QLabel(tr("label_min")))
            row.addWidget(lo)
            row.addWidget(QLabel(tr("label_max")))
            row.addWidget(hi)
            limits_form.addRow(f"{axis}:", row)
            self._spinboxes[axis] = (lo, hi)

        layout.addWidget(limits_box)

        advanced_box = QGroupBox(tr("group_advanced"))
        advanced_form = QFormLayout(advanced_box)

        self._rapid_feed_spin = QDoubleSpinBox()
        self._rapid_feed_spin.setRange(1.0, 100_000.0)
        self._rapid_feed_spin.setDecimals(1)
        self._rapid_feed_spin.setSuffix(" mm/min")
        self._rapid_feed_spin.valueChanged.connect(self._on_fields_edited)
        advanced_form.addRow(tr("label_rapid_feed"), self._rapid_feed_spin)

        self._default_feed_spin = QDoubleSpinBox()
        self._default_feed_spin.setRange(1.0, 100_000.0)
        self._default_feed_spin.setDecimals(1)
        self._default_feed_spin.setSuffix(" mm/min")
        self._default_feed_spin.valueChanged.connect(self._on_fields_edited)
        advanced_form.addRow(tr("label_default_feed"), self._default_feed_spin)

        self._min_feed_spin = QDoubleSpinBox()
        self._min_feed_spin.setRange(0.1, 10_000.0)
        self._min_feed_spin.setDecimals(2)
        self._min_feed_spin.setSuffix(" mm/min")
        self._min_feed_spin.valueChanged.connect(self._on_fields_edited)
        advanced_form.addRow(tr("label_min_feed"), self._min_feed_spin)

        self._arc_step_spin = QDoubleSpinBox()
        self._arc_step_spin.setRange(0.1, 45.0)
        self._arc_step_spin.setDecimals(1)
        self._arc_step_spin.setSuffix("°")
        self._arc_step_spin.valueChanged.connect(self._on_fields_edited)
        advanced_form.addRow(tr("label_arc_resolution"), self._arc_step_spin)

        layout.addWidget(advanced_box)
        layout.addStretch(1)

        self._load_active_into_fields()

    def profiles(self) -> list[MachineProfile]:
        return self._profiles

    def current_profile(self) -> MachineProfile:
        return self._active

    def _on_profile_selected(self, row: int) -> None:
        if row < 0:
            return
        self._active = self._profiles[row]
        self._load_active_into_fields()
        self.changed.emit()

    def _load_active_into_fields(self) -> None:
        self._loading = True
        self._mode_combo.setCurrentIndex(max(0, self._mode_combo.findData(self._active.mode_key)))
        self._dialect_combo.setCurrentIndex(
            max(0, self._dialect_combo.findData(self._active.dialect_key))
        )
        for axis, (lo, hi) in self._spinboxes.items():
            lo_value, hi_value = self._active.limits[axis]
            lo.setValue(lo_value)
            hi.setValue(hi_value)
        self._rapid_feed_spin.setValue(self._active.rapid_feed)
        self._default_feed_spin.setValue(self._active.default_feed)
        self._min_feed_spin.setValue(self._active.min_feed)
        self._arc_step_spin.setValue(self._active.arc_step_deg)
        self._loading = False

    def _on_fields_edited(self) -> None:
        if self._loading:
            return
        self._active.mode_key = self._mode_combo.currentData()
        self._active.dialect_key = self._dialect_combo.currentData()
        for axis, (lo, hi) in self._spinboxes.items():
            self._active.limits[axis] = (lo.value(), hi.value())
        self._active.rapid_feed = self._rapid_feed_spin.value()
        self._active.default_feed = self._default_feed_spin.value()
        self._active.min_feed = self._min_feed_spin.value()
        self._active.arc_step_deg = self._arc_step_spin.value()
        self.changed.emit()

    def _add_profile(self) -> None:
        name, ok = QInputDialog.getText(self, tr("dialog_new_profile_title"), tr("dialog_new_profile_label"))
        name = name.strip()
        if not ok or not name:
            return
        if any(p.name == name for p in self._profiles):
            QMessageBox.warning(self, tr("warn_name_used_title"), tr("warn_name_used_text").format(name=name))
            return

    def _remove_profile(self) -> None:
        if len(self._profiles) <= 1:
            QMessageBox.information(self, tr("info_cant_remove_title"), tr("info_cant_remove_text"))
            return
        row = self._profile_combo.currentIndex()
        if row < 0:
            return
        answer = QMessageBox.question(
            self, tr("confirm_remove_title"),
            tr("confirm_remove_text").format(name=self._profiles[row].name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

class _AppearancePage(QWidget):
    """Idioma da interface (reinicie o app para aplicar). Aqui também entrarão, no
    futuro, a cor de destaque (accent-color) e o tema claro."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(tr("appearance_language_label")))
        self._language_combo = QComboBox()
        for code, label in LANGUAGES:
            self._language_combo.addItem(label, code)
        self._language_combo.setCurrentIndex(
            max(0, self._language_combo.findData(get_language()))
        )
        layout.addWidget(self._language_combo)

        note = QLabel(tr("appearance_restart_note"))
        note.setWordWrap(True)
        layout.addWidget(note)
        layout.addStretch(1)

    def selected_language(self) -> str:
        return self._language_combo.currentData()

class _ShortcutsPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(tr("shortcuts_label")))
        text = QPlainTextEdit(_shortcuts_text())
        text.setReadOnly(True)
        layout.addWidget(text)


class SettingsDialog(QDialog):
    """Diálogo de Ajustes com navegação lateral entre seções."""

    profile_changed = Signal()

    def __init__(
        self,
        parent: QWidget | None = None,
        profiles: list[MachineProfile] | None = None,
        active_profile: MachineProfile | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("settings_title"))
        self.resize(560, 460)

        self._nav = QListWidget()
        self._nav.addItems([tr("nav_profiles"), tr("nav_shortcuts"), tr("nav_appearance")])
        self._nav.setFixedWidth(140)
        self._nav.currentRowChanged.connect(self._on_nav_changed)

        self._pages = QStackedWidget()
        self._profiles_page = _ProfilesPage(profiles or default_profiles(), active_profile)
        self._profiles_page.changed.connect(self.profile_changed.emit)
        self._pages.addWidget(self._profiles_page)
        self._pages.addWidget(_ShortcutsPage())
        self._appearance_page = _AppearancePage()
        self._pages.addWidget(self._appearance_page)

        body = QHBoxLayout()
        body.addWidget(self._nav)
        body.addWidget(self._pages, stretch=1)

        close_button = QPushButton(tr("btn_close"))
        close_button.clicked.connect(self.accept)

        button_row = QHBoxLayout()
        button_row.addStretch(1)
        button_row.addWidget(close_button)

        root = QVBoxLayout(self)
        root.addLayout(body)
        root.addLayout(button_row)

        self._nav.setCurrentRow(0)

    def _on_nav_changed(self, row: int) -> None:
        self._pages.setCurrentIndex(row)

    def profiles(self) -> list[MachineProfile]:
        return self._profiles_page.profiles()

    def current_profile(self) -> MachineProfile:
        return self._profiles_page.current_profile()

    def accept(self) -> None:
        self._save_language()
        super().accept()

    def _save_language(self) -> None:
        chosen = self._appearance_page.selected_language()
        set_language(chosen)  # já aplica aos textos que ainda forem montados nesta sessão
        try:
            config.SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
            config.SETTINGS_FILE.write_text(json.dumps({"language": chosen}), encoding="utf-8")
        except OSError:
            pass