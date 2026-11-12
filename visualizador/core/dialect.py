"""dialetos de G-code. as diferenças entre controladores ficam aqui, fora do núcleo.

cada perfil responde a perguntas sobre a máquina: em que unidade o G04 espera e
quais M-codes ligam e desligam o processo (spindle, arco, tocha). para uma máquina
nova, basta acrescentar um perfil em DIALECTS.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from core.lexer import clean_line

M_CODE_RE = re.compile(r"M\s*(\d+)")


@dataclass(frozen=True)
class Dialect:
    name: str
    dwell_unit: float           # segundos por unidade de P no G04
    process_on: frozenset[int]  # M-codes que ligam o processo
    process_off: frozenset[int] # M-codes que desligam o processo


DIALECTS: dict[str, Dialect] = {
    "generico": Dialect(
        name="Genérico (ISO)",
        dwell_unit=1.0,
        process_on=frozenset({3, 4}),   # M3/M4: spindle
        process_off=frozenset({5}),     # M5: spindle
    ),
    "arco-m8-m9": Dialect(
        name="Arco em M8/M9",
        dwell_unit=1.0,
        process_on=frozenset({8}),
        process_off=frozenset({9}),
    ),
    "fanuc": Dialect(
    name="Fanuc / Haas (P em milissegundos)",
    dwell_unit=0.001,            # G04 P é em ms nesses controladores, não em s
    process_on=frozenset({3, 4}),
    process_off=frozenset({5}),
    ),
    "plasma-m3-m5": Dialect(
        name="Plasma (tocha em M3/M5)",
        dwell_unit=1.0,
        process_on=frozenset({3}),   # plasma geralmente só liga em M3, sem M4
        process_off=frozenset({5}),
    ),
    "waam-m10-m11": Dialect(
        name="WAAM (arco em M10/M11)",
        dwell_unit=1.0,
        process_on=frozenset({10}),
        process_off=frozenset({11}),
    ),
}


def get_dialect(key: str) -> Dialect:
    try:
        return DIALECTS[key]
    except KeyError as err:
        raise ValueError(f"dialeto desconhecido: {key!r}") from err

DIALECT_CHOICES = [(dialect.name, key) for key, dialect in DIALECTS.items()]

_DIALECT_LABEL_KEYS = {
    "generico": "dialect_generic",
    "arco-m8-m9": "dialect_arc_m8_m9",
    "fanuc": "dialect_fanuc",
    "plasma-m3-m5": "dialect_plasma",
    "waam-m10-m11": "dialect_waam",
}

def dialect_label(key: str) -> str:
    from core.i18n import tr
    return tr(_DIALECT_LABEL_KEYS.get(key, get_dialect(key).name))


def process_codes_label(key: str) -> str:
    """códigos de liga/desliga do dialeto, para mostrar ao usuário: 'M8/M9'."""
    dialect = get_dialect(key)
    return "/".join(f"M{code}" for code in (*sorted(dialect.process_on), *sorted(dialect.process_off)))


def m_codes_in(text: str) -> set[int]:
    """M-codes presentes no programa, ignorando comentários."""
    codes: set[int] = set()
    for raw in text.splitlines():
        codes.update(int(number) for number in M_CODE_RE.findall(clean_line(raw)))
    return codes


def suggest_dialect(text: str, current_key: str) -> str | None:
    """dialeto que combina com o arquivo quando o atual não combina.

    só sugere se o programa não usa nenhum código de ligar do dialeto atual e
    usa os de ligar e de desligar de outro. assim um M8 de refrigeração em um
    programa com M3/M5 não dispara a sugestão.
    """
    used = m_codes_in(text)
    if used & get_dialect(current_key).process_on:
        return None
    for key, dialect in DIALECTS.items():
        if key != current_key and used & dialect.process_on and used & dialect.process_off:
            return key
    return None


def dialect_choices() -> list[tuple[str, str]]:
    from core.i18n import tr  # import tardio: evita ciclo e garante tradução na hora certa
    return [
        (tr(_DIALECT_LABEL_KEYS.get(key, dialect.name)), key)
        for key, dialect in DIALECTS.items()
    ]