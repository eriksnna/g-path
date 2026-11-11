"""Leitura de arquivos G-code preservando a codificação original. Não depende de Qt."""
from __future__ import annotations

import codecs
from pathlib import Path

FALLBACK_ENCODINGS = ("utf-8", "cp1252", "latin-1")  # latin-1 aceita qualquer byte


def read_gcode_text(path: Path) -> tuple[str, str]:
    """Devolve (texto, codificação) para que o salvamento use a mesma codificação."""
    data = path.read_bytes()
    if data.startswith(codecs.BOM_UTF8):
        return data.decode("utf-8-sig"), "utf-8-sig"
    for encoding in FALLBACK_ENCODINGS:
        try:
            return data.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    raise AssertionError("latin-1 decodifica qualquer sequência de bytes")