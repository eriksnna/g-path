"""texto vindo de fora (arquivo, caminho, nome de perfil) exibido sem interpretar marcação."""
from __future__ import annotations

from html import escape


def plain_tooltip(text: str) -> str:
    """tooltip que mostra o texto ao pé da letra.

    o Qt trata como HTML qualquer tooltip que pareça ter uma tag. um caminho ou uma
    linha de G-code com "<...>" seria interpretado em vez de exibido.
    """
    return f"<span>{escape(text).replace(chr(10), '<br>')}</span>" if text else ""