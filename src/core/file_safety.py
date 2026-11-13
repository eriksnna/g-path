"""Verificações de segurança antes de interpretar um arquivo G-code.

G-code é entrada não confiável: pode vir de qualquer origem. Este módulo recusa
arquivos fora de limites razoáveis antes que o parser/expander gastem memória ou
tempo com eles. Não depende de Qt.
"""
from __future__ import annotations

from pathlib import Path

from core.i18n import tr

from config import MAX_FILE_SIZE_BYTES, MAX_LINE_LENGTH


class UnsafeFileError(ValueError):
    """o arquivo foi recusado por exceder um limite de segurança."""


def check_file_size(path: Path) -> None:
    size = path.stat().st_size
    if size > MAX_FILE_SIZE_BYTES:
        raise UnsafeFileError(tr("file_too_large").format(
            size=f"{size / 1_048_576:.1f}", limit=f"{MAX_FILE_SIZE_BYTES / 1_048_576:.0f}",
        ))


def check_line_lengths(text: str) -> None:
    for lineno, line in enumerate(text.splitlines(), start=1):
        if len(line) > MAX_LINE_LENGTH:
            raise UnsafeFileError(tr("file_line_too_long").format(
                line=lineno, length=len(line), limit=MAX_LINE_LENGTH)
            )