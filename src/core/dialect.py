"""dialetos de G-code. as diferenças entre controladores ficam aqui, fora do núcleo.

cada perfil responde a perguntas sobre a máquina: em que unidade o G04 espera e
quais M-codes ligam e desligam o processo (spindle, arco, tocha). além dos prontos em
DIALECTS, cada perfil de máquina guarda um dialeto personalizado, editável nos Ajustes.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from core.lexer import clean_line

M_CODE_RE = re.compile(r"M\s*(\d+)")

CUSTOM_DIALECT = "personalizado"   # chave do dialeto que o usuário define no perfil
SECONDS, MILLISECONDS = 1.0, 0.001  # unidades aceitas para o P do G04
DWELL_UNITS = (SECONDS, MILLISECONDS)
MAX_M_CODE = 999
MAX_PROCESS_CODES = 8
# pausa, fim de programa e sub-rotinas: o interpretador já usa esses, não podem ligar o processo
RESERVED_M_CODES = frozenset({0, 1, 2, 30, 98, 99})
_CODE_TEXT_RE = re.compile(r"M?\s*(\d+)", re.IGNORECASE)
_CODE_SEPARATORS_RE = re.compile(r"[\s,;/]+")

class DialectError(ValueError):
    """dialeto personalizado inválido. a mensagem já vem traduzida, pronta para a tela."""


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

def parse_m_codes(text: str) -> frozenset[int]:
    """lê o que o usuário digitou: 'M10', 'M10, M12', '10 12' ou 'm10/m12'."""
    from core.i18n import tr
    codes = set()
    for part in _CODE_SEPARATORS_RE.split(text.strip()):
        if not part:
            continue
        match = _CODE_TEXT_RE.fullmatch(part)
        if match is None:
            raise DialectError(tr("dialect_error_not_code").format(text=part))
        codes.add(int(match.group(1)))
    return frozenset(codes)


def format_m_codes(codes) -> str:
    return ", ".join(f"M{code}" for code in sorted(codes))


def make_custom_dialect(process_on, process_off, dwell_unit: float) -> Dialect:
    from core.i18n import tr
    on, off = _valid_codes(process_on), _valid_codes(process_off)
    if not on or not off:
        raise DialectError(tr("dialect_error_empty"))
    if on & off:
        raise DialectError(tr("dialect_error_overlap").format(codes=format_m_codes(on & off)))
    reserved = (on | off) & RESERVED_M_CODES
    if reserved:
        raise DialectError(tr("dialect_error_reserved").format(codes=format_m_codes(reserved)))
    if dwell_unit not in DWELL_UNITS:
        raise DialectError(tr("dialect_error_dwell_unit"))
    return Dialect(name=CUSTOM_DIALECT, dwell_unit=dwell_unit, process_on=on, process_off=off)


def default_custom_dialect() -> Dialect:
    """ponto de partida do personalizado: os mesmos códigos do genérico."""
    generic = DIALECTS["generico"]
    return make_custom_dialect(generic.process_on, generic.process_off, generic.dwell_unit)


def _valid_codes(codes) -> frozenset[int]:
    from core.i18n import tr
    try:
        result = frozenset(int(code) for code in codes)
    except (TypeError, ValueError) as err:
        raise DialectError(tr("dialect_error_empty")) from err
    if len(result) > MAX_PROCESS_CODES or any(not 0 <= code <= MAX_M_CODE for code in result):
        raise DialectError(tr("dialect_error_range").format(limit=MAX_PROCESS_CODES, highest=MAX_M_CODE))
    return result

def get_dialect(key: str) -> Dialect:
    try:
        return DIALECTS[key]
    except KeyError as err:
        raise ValueError(f"dialeto desconhecido: {key!r}") from err

_DIALECT_LABEL_KEYS = {
    "generico": "dialect_generic",
    "arco-m8-m9": "dialect_arc_m8_m9",
    "fanuc": "dialect_fanuc",
    "plasma-m3-m5": "dialect_plasma",
    "waam-m10-m11": "dialect_waam",
    CUSTOM_DIALECT: "dialect_custom",
}

def dialect_label(key: str) -> str:
    from core.i18n import tr
    return tr(_DIALECT_LABEL_KEYS[key]) if key in _DIALECT_LABEL_KEYS else get_dialect(key).name


def process_codes_label(dialect: Dialect) -> str:
    """códigos de liga/desliga do dialeto, para mostrar ao usuário: 'M8/M9'."""
    return "/".join(f"M{code}" for code in (*sorted(dialect.process_on), *sorted(dialect.process_off)))


def m_codes_in(text: str) -> set[int]:
    """M-codes presentes no programa, ignorando comentários."""
    codes: set[int] = set()
    for raw in text.splitlines():
        codes.update(int(number) for number in M_CODE_RE.findall(clean_line(raw)))
    return codes


def suggest_dialect(text: str, current: Dialect) -> str | None:
    """dialeto que combina com o arquivo quando o atual não combina.

    só sugere se o programa não usa nenhum código de ligar do dialeto atual e
    usa os de ligar e de desligar de outro. assim um M8 de refrigeração em um
    programa com M3/M5 não dispara a sugestão.
    """
    used = m_codes_in(text)
    if used & current.process_on:
        return None
    for key, dialect in DIALECTS.items():
        if dialect is not current and used & dialect.process_on and used & dialect.process_off:
            return key
    return None


def dialect_choices() -> list[tuple[str, str]]:
    from core.i18n import tr  # import tardio: evita ciclo e garante tradução na hora certa
    choices = [
        (tr(_DIALECT_LABEL_KEYS.get(key, dialect.name)), key)
        for key, dialect in DIALECTS.items()
    ]
    return [*choices, (tr(_DIALECT_LABEL_KEYS[CUSTOM_DIALECT]), CUSTOM_DIALECT)]