"""painel de validação: lista os problemas e leva o usuário até a linha no caminho."""
from __future__ import annotations

from core.i18n import tr

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QFrame, QLabel, QListWidget, QListWidgetItem, QVBoxLayout,
)

from core.parser import ERROR, WARNING, Issue
from ui.theme import ERROR_COLOR, WARNING_COLOR

PANEL_WIDTH = 300
LINE_ROLE = Qt.ItemDataRole.UserRole
_SEVERITY_LABELS = {ERROR: "severity_error", WARNING: "severity_warning"}


class IssuesPanel(QFrame):
    issue_selected = Signal(int)  # número da linha

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("issuesPanel")
        self.setMinimumWidth(PANEL_WIDTH)

        title = QLabel(tr("validation_title"))
        title.setObjectName("sectionTitle")

        self._summary = QLabel()
        self._summary.setObjectName("issueSummary")

        self._list = QListWidget()
        self._list.setObjectName("issues")
        self._list.setWordWrap(True)
        self._list.setResizeMode(QListWidget.ResizeMode.Adjust)
        self._list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._list.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self._list.itemClicked.connect(self._on_clicked)

        self._empty = QLabel(tr("validation_empty"))
        self._empty.setObjectName("issueEmpty")

        self._detail = QLabel(tr("validation_hint"))
        self._detail.setObjectName("issueDetail")
        self._detail.setWordWrap(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(8)
        layout.addWidget(title)
        layout.addWidget(self._summary)
        layout.addWidget(self._list, 1)
        layout.addWidget(self._empty)
        layout.addWidget(self._detail)

        self.show_issues([])

    def show_issues(self, issues: list[Issue]) -> None:
        self._list.clear()
        for issue in issues:
            item = QListWidgetItem(f"L{issue.line}   {issue.message}")
            item.setData(LINE_ROLE, issue.line)
            color = ERROR_COLOR if issue.severity == ERROR else WARNING_COLOR
            item.setForeground(QColor(color))
            item.setToolTip(f"{tr(_SEVERITY_LABELS.get(issue.severity, issue.severity))}: {issue.message}")
            self._list.addItem(item)

        errors = sum(1 for issue in issues if issue.severity == ERROR)
        warnings = len(issues) - errors
        has_issues = bool(issues)

        self._list.setVisible(has_issues)
        self._empty.setVisible(not has_issues)
        self._detail.setVisible(has_issues)
        self._summary.setText(
            tr("validation_summary").format(errors=errors, warnings=warnings) if has_issues else ""
        )
        self._detail.setText(tr("validation_hint"))

    def show_source(self, line: int, text: str) -> None:
        self._detail.setText(
            tr("validation_line_prefix").format(line=line, text=text or tr("validation_empty_line"))
        )

    def _on_clicked(self, item: QListWidgetItem) -> None:
        self.issue_selected.emit(item.data(LINE_ROLE))