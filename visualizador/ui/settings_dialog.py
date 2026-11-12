"""tela de ajustes: navegação lateral com seções (perfis, atalhos, aparência, sobre).

cada perfil reúne modo de processo, dialeto e limites de curso: a configuração
completa de uma máquina.
"""
from __future__ import annotations

import json

from PySide6.QtCore import QLocale, Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QComboBox, QDialog, QDoubleSpinBox, QFrame, QGridLayout, QHBoxLayout, QInputDialog,
    QLabel, QListWidget, QMessageBox, QPushButton, QStackedWidget, QVBoxLayout, QWidget,
)

import config
from core.dialect import dialect_choices
from core.i18n import LANGUAGES, get_language, set_language, tr
from core.machine_profile import MachineProfile, default_profiles
from core.modes import mode_choices
from ui.theme import ACCENT_TEXT, SPACE_LG, SPACE_MD, SPACE_SM, SPACE_XL, SPACE_XXL

DIALOG_SIZE = (620, 540)
NAV_WIDTH = 140
LABEL_WIDTH = 120   # mesma largura em todos os cartões: os campos ficam alinhados entre si
ABOUT_LOGO_SIZE = 44
AXES = ("X", "Y", "Z")
NUMBER_LOCALE = QLocale(QLocale.Language.C)  # ponto decimal, como no resto do programa

THIRD_PARTY = (
    ("Qt for Python (PySide6)", "LGPL-3.0"),
    ("pyqtgraph", "MIT"),
    ("NumPy", "BSD-3-Clause"),
    ("PyOpenGL", "BSD-3-Clause"),
    ("Phosphor Icons", "MIT"),
)


def _section_title(text: str) -> QLabel:
    label = QLabel(text.upper())
    label.setObjectName("sectionTitle")
    return label


def _card() -> tuple[QFrame, QGridLayout]:
    """Cartão com uma grade de duas ou mais colunas; a primeira é a dos rótulos."""
    card = QFrame()
    card.setObjectName("settingsCard")
    grid = QGridLayout(card)
    grid.setContentsMargins(SPACE_XL, SPACE_LG, SPACE_XL, SPACE_LG)
    grid.setHorizontalSpacing(SPACE_MD)
    grid.setVerticalSpacing(SPACE_SM)
    grid.setColumnMinimumWidth(0, LABEL_WIDTH)
    return card, grid


def _spin(minimum: float, maximum: float, decimals: int, suffix: str = "") -> QDoubleSpinBox:
    spin = QDoubleSpinBox()
    spin.setLocale(NUMBER_LOCALE)
    spin.setGroupSeparatorShown(False)
    spin.setRange(minimum, maximum)
    spin.setDecimals(decimals)
    spin.setSuffix(suffix)
    return spin


def _page_layout(page: QWidget) -> QVBoxLayout:
    layout = QVBoxLayout(page)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(SPACE_SM)
    return layout


class _ProfilesPage(QWidget):
    """lista de perfis: cada perfil reúne modo, dialeto e limites de curso."""

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

        self._profile_combo = QComboBox()
        for profile in self._profiles:
            self._profile_combo.addItem(profile.name)
        start_row = self._profiles.index(self._active) if self._active in self._profiles else 0
        self._profile_combo.setCurrentIndex(start_row)
        self._profile_combo.currentIndexChanged.connect(self._on_profile_selected)
        add_button = QPushButton(tr("btn_save_as_profile"))
        add_button.clicked.connect(self._add_profile)
        remove_button = QPushButton(tr("btn_remove_profile"))
        remove_button.setObjectName("linkDanger")  # ação destrutiva: discreta, longe da principal
        remove_button.clicked.connect(self._remove_profile)
        profile_row = QHBoxLayout()
        profile_row.setSpacing(SPACE_SM)
        profile_row.addWidget(self._profile_combo, 1)
        profile_row.addWidget(add_button)

        self._mode_combo = QComboBox()
        for label, key in mode_choices():
            self._mode_combo.addItem(label, key)
        self._dialect_combo = QComboBox()
        for label, key in dialect_choices():
            self._dialect_combo.addItem(label, key)
        config_card, config_grid = _card()
        config_grid.addWidget(QLabel(tr("label_mode_colon")), 0, 0)
        config_grid.addWidget(self._mode_combo, 0, 1)
        config_grid.addWidget(QLabel(tr("label_dialect_colon")), 1, 0)
        config_grid.addWidget(self._dialect_combo, 1, 1)
        config_grid.setColumnStretch(1, 1)

        limits_card, limits_grid = _card()
        for column, key in ((1, "label_min"), (2, "label_max")):
            caption = QLabel(tr(key))
            caption.setObjectName("fieldCaption")
            limits_grid.addWidget(caption, 0, column)
        for row, axis in enumerate(AXES, start=1):
            lo = _spin(-1_000_000.0, 1_000_000.0, 2)
            hi = _spin(-1_000_000.0, 1_000_000.0, 2)
            limits_grid.addWidget(QLabel(axis), row, 0)
            limits_grid.addWidget(lo, row, 1)
            limits_grid.addWidget(hi, row, 2)
            self._spinboxes[axis] = (lo, hi)
        limits_grid.setColumnStretch(1, 1)
        limits_grid.setColumnStretch(2, 1)

        self._rapid_feed_spin = _spin(1.0, 100_000.0, 1, " mm/min")
        self._default_feed_spin = _spin(1.0, 100_000.0, 1, " mm/min")
        self._min_feed_spin = _spin(0.1, 10_000.0, 2, " mm/min")
        self._arc_step_spin = _spin(0.1, 45.0, 1, "°")
        advanced_card, advanced_grid = _card()
        advanced_fields = (
            ("label_rapid_feed", self._rapid_feed_spin),
            ("label_default_feed", self._default_feed_spin),
            ("label_min_feed", self._min_feed_spin),
            ("label_arc_resolution", self._arc_step_spin),
        )
        for row, (key, spin) in enumerate(advanced_fields):
            advanced_grid.addWidget(QLabel(tr(key)), row, 0)
            advanced_grid.addWidget(spin, row, 1)
        advanced_grid.setColumnStretch(1, 1)

        for widget in (self._mode_combo, self._dialect_combo):
            widget.currentIndexChanged.connect(self._on_fields_edited)
        spins = [spin for pair in self._spinboxes.values() for spin in pair]
        for spin in (*spins, *(spin for _, spin in advanced_fields)):
            spin.valueChanged.connect(self._on_fields_edited)

        layout = _page_layout(self)
        layout.addWidget(_section_title(tr("profile_combo_label").rstrip(":")))
        layout.addLayout(profile_row)
        layout.addSpacing(SPACE_SM)
        layout.addWidget(_section_title(tr("group_profile_config")))
        layout.addWidget(config_card)
        layout.addWidget(_section_title(tr("group_travel_limits")))
        layout.addWidget(limits_card)
        layout.addWidget(_section_title(tr("group_advanced")))
        layout.addWidget(advanced_card)
        layout.addStretch(1)
        layout.addWidget(remove_button, 0, Qt.AlignmentFlag.AlignLeft)

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
        """Novo perfil com os valores do atual, sob outro nome."""
        name, ok = QInputDialog.getText(self, tr("dialog_new_profile_title"), tr("dialog_new_profile_label"))
        name = name.strip()
        if not ok or not name:
            return
        if any(p.name == name for p in self._profiles):
            QMessageBox.warning(self, tr("warn_name_used_title"), tr("warn_name_used_text").format(name=name))
            return
        profile = self._active.clone()
        profile.name = name
        self._profiles.append(profile)
        self._profile_combo.addItem(name)
        self._profile_combo.setCurrentIndex(len(self._profiles) - 1)  # dispara _on_profile_selected

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
        if answer != QMessageBox.StandardButton.Yes:
            return
        del self._profiles[row]
        self._profile_combo.blockSignals(True)
        self._profile_combo.removeItem(row)
        self._profile_combo.setCurrentIndex(min(row, len(self._profiles) - 1))
        self._profile_combo.blockSignals(False)
        self._on_profile_selected(self._profile_combo.currentIndex())


class _ShortcutsPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        sections = (
            ("shortcuts_section_player", (
                ("Space", "shortcut_play_pause"),
                ("←  →", "shortcut_step_move"),
                ("Shift + ←  →", "shortcut_step_layer"),
                ("Home  End", "shortcut_start_end"),
            )),
            ("shortcuts_section_editor", (
                ("Ctrl + Enter", "editor_shortcut_apply"),
                ("Ctrl + S", "editor_shortcut_save"),
                ("Ctrl + Shift + S", "editor_shortcut_save_as"),
                ("Ctrl + F", "editor_shortcut_find"),
                ("Ctrl + /", "editor_shortcut_comment"),
            )),
        )
        layout = _page_layout(self)
        for title_key, shortcuts in sections:
            card, grid = _card()
            for row, (keys, description_key) in enumerate(shortcuts):
                key_label = QLabel(keys)
                key_label.setObjectName("kbd")
                grid.addWidget(key_label, row, 0, Qt.AlignmentFlag.AlignLeft)
                grid.addWidget(QLabel(tr(description_key)), row, 1)
            grid.setColumnStretch(1, 1)
            layout.addWidget(_section_title(tr(title_key)))
            layout.addWidget(card)
        layout.addStretch(1)


class _AppearancePage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._language_combo = QComboBox()
        for code, label in LANGUAGES:
            self._language_combo.addItem(label, code)
        self._language_combo.setCurrentIndex(
            max(0, self._language_combo.findData(get_language()))
        )
        note = QLabel(tr("appearance_restart_note"))
        note.setObjectName("fieldCaption")
        note.setWordWrap(True)

        card, grid = _card()
        grid.addWidget(QLabel(tr("appearance_language_label")), 0, 0)
        grid.addWidget(self._language_combo, 0, 1)
        grid.addWidget(note, 1, 1)
        grid.setColumnStretch(1, 1)

        layout = _page_layout(self)
        layout.addWidget(_section_title(tr("nav_appearance")))
        layout.addWidget(card)
        layout.addStretch(1)

    def selected_language(self) -> str:
        return self._language_combo.currentData()


class _AboutPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        logo = QLabel()
        logo.setPixmap(QPixmap(str(config.ASSETS_DIR / "logo.png")).scaled(
            ABOUT_LOGO_SIZE, ABOUT_LOGO_SIZE,
            Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation,
        ))
        name = QLabel(config.APP_TITLE)
        name.setObjectName("aboutTitle")
        version = QLabel(f"v{config.APP_VERSION}")
        version.setObjectName("fieldCaption")
        heading = QVBoxLayout()
        heading.setSpacing(0)
        heading.addWidget(name)
        heading.addWidget(version)
        header = QHBoxLayout()
        header.setSpacing(SPACE_LG)
        header.addWidget(logo)
        header.addLayout(heading)
        header.addStretch()

        description = QLabel(tr("start_subtitle"))
        description.setWordWrap(True)

        links = [(tr("about_source_code"), config.GITHUB_URL), ("LinkedIn", config.LINKEDIN_URL)]
        links_html = "&nbsp;&nbsp;·&nbsp;&nbsp;".join(
            f'<a href="{url}" style="color:{ACCENT_TEXT}; text-decoration:none">{label}</a>'
            for label, url in links if url
        )
        author = QLabel(f"{tr('about_author').format(name=config.AUTHOR_NAME)}<br>{links_html}")
        author.setTextFormat(Qt.TextFormat.RichText)
        author.setOpenExternalLinks(True)
        author_card, author_grid = _card()
        author_grid.addWidget(author, 0, 0, 1, 2)

        license_card, license_grid = _card()
        license_grid.addWidget(QLabel(config.APP_TITLE), 0, 0)
        license_grid.addWidget(QLabel("MIT"), 0, 1)
        for row, (library, license_name) in enumerate(THIRD_PARTY, start=1):
            license_grid.addWidget(QLabel(library), row, 0)
            license_grid.addWidget(QLabel(license_name), row, 1)
        license_grid.setColumnMinimumWidth(0, 200)
        license_grid.setColumnStretch(1, 1)
        license_note = QLabel(tr("about_license_note"))
        license_note.setObjectName("fieldCaption")
        license_note.setWordWrap(True)

        layout = _page_layout(self)
        layout.addLayout(header)
        layout.addWidget(description)
        layout.addSpacing(SPACE_SM)
        layout.addWidget(_section_title(tr("about_section_author")))
        layout.addWidget(author_card)
        layout.addWidget(_section_title(tr("about_section_licenses")))
        layout.addWidget(license_card)
        layout.addWidget(license_note)
        layout.addStretch(1)


class SettingsDialog(QDialog):
    """diálogo de ajustes com navegação lateral entre seções."""

    profile_changed = Signal()

    def __init__(
        self,
        parent: QWidget | None = None,
        profiles: list[MachineProfile] | None = None,
        active_profile: MachineProfile | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("settings_title"))
        self.resize(*DIALOG_SIZE)

        self._nav = QListWidget()
        self._nav.setObjectName("settingsNav")
        self._nav.addItems([
            tr("nav_profiles"), tr("nav_shortcuts"), tr("nav_appearance"), tr("nav_about"),
        ])
        self._nav.setFixedWidth(NAV_WIDTH)
        self._nav.currentRowChanged.connect(self._on_nav_changed)

        self._pages = QStackedWidget()
        self._profiles_page = _ProfilesPage(profiles or default_profiles(), active_profile)
        self._profiles_page.changed.connect(self.profile_changed.emit)
        self._appearance_page = _AppearancePage()
        for page in (self._profiles_page, _ShortcutsPage(), self._appearance_page, _AboutPage()):
            self._pages.addWidget(page)

        body = QHBoxLayout()
        body.setSpacing(SPACE_XXL)
        body.addWidget(self._nav)
        body.addWidget(self._pages, stretch=1)

        close_button = QPushButton(tr("btn_close"))
        close_button.clicked.connect(self.accept)
        button_row = QHBoxLayout()
        button_row.addStretch(1)
        button_row.addWidget(close_button)

        root = QVBoxLayout(self)
        root.setContentsMargins(SPACE_XXL, SPACE_XXL, SPACE_XXL, SPACE_XL)
        root.setSpacing(SPACE_LG)
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