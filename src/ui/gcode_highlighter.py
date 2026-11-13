"""realce de sintaxe para G-code: comentários, G/M-codes, eixos, variáveis e sub-rotinas."""
from __future__ import annotations

from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat

from ui import theme

# ordem importa: comentários são aplicados por último, para cobrir qualquer coisa dentro deles.
COMMENT_PAREN_RE = QRegularExpression(r"\([^)]*\)")
COMMENT_SEMI_RE = QRegularExpression(r";.*$")
SUBROUTINE_LABEL_RE = QRegularExpression(r"^\s*O\d+\b")
G_CODE_RE = QRegularExpression(r"\bG\d+(\.\d+)?\b")
M_CODE_RE = QRegularExpression(r"\bM\d+\b")
AXIS_RE = QRegularExpression(r"\b[XYZIJKR][-+]?\d+(\.\d+)?\b")
FEED_SPEED_RE = QRegularExpression(r"\b[FS][-+]?\d+(\.\d+)?\b")
CALL_PARAM_RE = QRegularExpression(r"\b[PL][-+]?\d+(\.\d+)?\b")
VARIABLE_RE = QRegularExpression(r"#\d+")
NUMBER_RE = QRegularExpression(r"(?<![A-Za-z#])[-+]?\d+\.\d+\b")


def _format(color: str, bold: bool = False, italic: bool = False) -> QTextCharFormat:
    fmt = QTextCharFormat()
    fmt.setForeground(QColor(color))
    if bold:
        fmt.setFontWeight(QFont.Weight.Bold)
    if italic:
        fmt.setFontItalic(True)
    return fmt


class GCodeHighlighter(QSyntaxHighlighter):
    def __init__(self, document) -> None:
        super().__init__(document)
        self._rules = [
            (SUBROUTINE_LABEL_RE, _format(theme.SYNTAX_LABEL, bold=True)),
            (G_CODE_RE, _format(theme.SYNTAX_G_CODE, bold=True)),
            (M_CODE_RE, _format(theme.SYNTAX_M_CODE, bold=True)),
            (AXIS_RE, _format(theme.SYNTAX_AXIS)),
            (FEED_SPEED_RE, _format(theme.SYNTAX_PARAM)),
            (CALL_PARAM_RE, _format(theme.SYNTAX_PARAM)),
            (VARIABLE_RE, _format(theme.SYNTAX_VARIABLE, bold=True)),
            (NUMBER_RE, _format(theme.SYNTAX_NUMBER)),
        ]
        self._comment_format = _format(theme.SYNTAX_COMMENT, italic=True)

    def highlightBlock(self, text: str) -> None:
        for pattern, fmt in self._rules:
            self._apply(pattern, text, fmt)
        self._highlight_comments(text)

    def _apply(self, pattern: QRegularExpression, text: str, fmt: QTextCharFormat) -> None:
        it = pattern.globalMatch(text)
        while it.hasNext():
            match = it.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

    def _highlight_comments(self, text: str) -> None:
        """comentários sobrepõem qualquer outro realce que caia dentro deles."""
        it = COMMENT_PAREN_RE.globalMatch(text)
        while it.hasNext():
            match = it.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self._comment_format)

        semi_match = COMMENT_SEMI_RE.match(text)
        if semi_match.hasMatch():
            start = semi_match.capturedStart()
            self.setFormat(start, len(text) - start, self._comment_format)