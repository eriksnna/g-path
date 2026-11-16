"""leitura e gravação de arquivos de texto: preserva a codificação e não corrompe o original."""
from __future__ import annotations

import codecs
import os
import shutil
import tempfile
from pathlib import Path

FALLBACK_ENCODINGS = ("utf-8", "cp1252", "latin-1")  # latin-1 aceita qualquer byte


def read_gcode_text(path: Path) -> tuple[str, str]:
    data = path.read_bytes()
    if data.startswith(codecs.BOM_UTF8):
        return _unix_newlines(data.decode("utf-8-sig")), "utf-8-sig"
    for encoding in FALLBACK_ENCODINGS:
        try:
            return _unix_newlines(data.decode(encoding)), encoding
        except UnicodeDecodeError:
            continue
    raise AssertionError("latin-1 decodifica qualquer sequência de bytes")


def _unix_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def write_text_atomic(path: Path, text: str, encoding: str) -> None:
    """grava em um arquivo temporário na mesma pasta e só então troca pelo original.
    se algo falhar no meio, o original fica intacto."""
    text.encode(encoding)
    target = Path(os.path.realpath(path))
    handle, temp_name = tempfile.mkstemp(dir=target.parent, prefix=target.name + ".", suffix=".tmp")
    try:
        with os.fdopen(handle, "w", encoding=encoding) as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        if target.exists():
            shutil.copymode(target, temp_name)
        os.replace(temp_name, target)
    except BaseException:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise