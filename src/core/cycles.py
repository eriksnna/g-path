"""ciclos fixos de furação (G73, G81, G82, G83): o percurso em Z de um furo, já na posição XY."""
from __future__ import annotations

from dataclasses import dataclass

from core.i18n import tr
from core.lexer import GCodeError

G_CHIP_BREAK = 73   # bicadas curtas, recuando só um pouco
G_DRILL = 81
G_DRILL_DWELL = 82  # espera no fundo
G_PECK = 83         # bicadas, voltando ao plano R entre elas
DRILL_CYCLES = {G_CHIP_BREAK, G_DRILL, G_DRILL_DWELL, G_PECK}
PECK_CYCLES = {G_CHIP_BREAK, G_PECK}

CHIP_BREAK_RETRACT = 0.5  # mm que o G73 recua entre bicadas
PECK_CLEARANCE = 0.5      # mm acima do fundo anterior onde o G83 volta a avançar
MAX_PECKS = 10_000        # Q minúsculo em furo fundo não pode gerar trechos sem fim

RAPID = "rapid"
FEED = "feed"
DWELL = "dwell"


@dataclass(frozen=True)
class Step:
    kind: str   # RAPID, FEED ou DWELL
    z: float    # altura ao fim do trecho


def drill_steps(code: int, r_level: float, bottom: float, retract: float, peck: float) -> list[Step]:
    """trechos em Z de um furo: desce ao plano R, fura até o fundo e recua."""
    if bottom > r_level:
        raise GCodeError(tr("issue_cycle_bottom_above_r").format(code=code))
    if code in PECK_CYCLES and peck <= 0:
        raise GCodeError(tr("issue_cycle_missing_q").format(code=code))

    steps = [Step(RAPID, r_level)]
    if code in PECK_CYCLES:
        peck = max(peck, (r_level - bottom) / MAX_PECKS)
        depth = r_level
        while depth > bottom:
            target = max(depth - peck, bottom)
            if code == G_PECK and depth < r_level:
                steps.append(Step(RAPID, depth + PECK_CLEARANCE))
            steps.append(Step(FEED, target))
            if target > bottom:
                steps.append(Step(RAPID, r_level if code == G_PECK else target + CHIP_BREAK_RETRACT))
            depth = target
    else:
        steps.append(Step(FEED, bottom))
        if code == G_DRILL_DWELL:
            steps.append(Step(DWELL, bottom))
    steps.append(Step(RAPID, retract))
    return steps