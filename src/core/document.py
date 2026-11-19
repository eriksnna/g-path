"""o programa aberto: caminho, texto, codificação e o que já está gravado em disco. sem Qt."""
from __future__ import annotations

from pathlib import Path

from core.file_io import read_gcode_text, write_text_atomic
from core.file_safety import check_file_size, check_line_lengths

DEFAULT_ENCODING = "utf-8"


def read_program(path: Path) -> tuple[str, str]:
    """lê um G-code com as checagens de tamanho. levanta UnsafeFileError ou OSError."""
    check_file_size(path)
    text, encoding = read_gcode_text(path)
    check_line_lengths(text)
    return text, encoding


class Document:
    def __init__(self) -> None:
        self.path: Path | None = None        # None: programa novo, ainda sem arquivo
        self.text: str | None = None         # None: nenhum programa aberto
        self.saved_text: str | None = None   # o que está gravado em disco
        self.encoding = DEFAULT_ENCODING     # salvar reaproveita a codificação lida

    def open(self, path: Path) -> None:
        """carrega um arquivo. se a leitura falhar, levanta o erro e nada muda."""
        text, encoding = read_program(path)
        self.path, self.text, self.saved_text, self.encoding = path, text, text, encoding

    def new_blank(self) -> None:
        self.path, self.text, self.saved_text, self.encoding = None, "", "", DEFAULT_ENCODING

    def close(self) -> None:
        self.path, self.text, self.saved_text = None, None, None

    def apply(self, text: str) -> None:
        """o texto editado passa a ser o programa simulado, mesmo sem salvar."""
        self.text = text

    def save(self, text: str, path: Path | None = None) -> None:
        """grava no caminho dado ou no atual. levanta OSError; se falhar, nada muda."""
        target = path or self.path
        if target is None:
            raise ValueError("documento sem caminho: informe onde salvar")
        encoding = self.encoding
        try:
            write_text_atomic(target, text, encoding)
        except UnicodeEncodeError:
            # o texto novo tem caractere que a codificação original não comporta
            encoding = DEFAULT_ENCODING
            write_text_atomic(target, text, encoding)
        self.path, self.text, self.saved_text, self.encoding = target, text, text, encoding

    def has_unsaved_changes(self, editor_modified: bool = False) -> bool:
        if self.text is None:
            return False
        return editor_modified or self.text != self.saved_text

    def changed_on_disk(self) -> tuple[str, str] | None:
        """relê o arquivo; devolve (texto, codificação) só se o conteúdo for outro."""
        if self.path is None:
            return None
        try:
            text, encoding = read_program(self.path)
        except (ValueError, OSError):  # UnsafeFileError herda de ValueError
            return None
        return None if text == self.saved_text else (text, encoding)

    def take_disk_version(self, text: str, encoding: str) -> None:
        self.text, self.saved_text, self.encoding = text, text, encoding