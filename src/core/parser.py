"""interpretação de movimentos G-code.

sub-rotinas e variáveis já foram expandidas por core.expander. os códigos de
processo (M-codes) são traduzidos pelo dialeto escolhido, não fixados aqui.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from config import ARC_STEP_DEG, DEFAULT_DIALECT, DEFAULT_FEED, INCH_TO_MM, MAX_MOVES
from core.machine_profile import DEFAULT_LIMITS as MACHINE_LIMITS
from core.cycles import DRILL_CYCLES, DWELL, RAPID, drill_steps
from core.dialect import Dialect, get_dialect
from core.expander import expand_program
from core.i18n import tr
from core.lexer import ERROR, WARNING, GCodeError, Issue, clean_line, parse_words

Point = tuple[float, float, float]
Limits = dict[str, tuple[float, float]]

G_RAPID = 0
G_LINEAR = 1
G_CW_ARC = 2
G_CCW_ARC = 3
G_DWELL = 4
DWELL_SECONDS_WORDS = ("X", "U")
G_UNITS = {20: INCH_TO_MM, 21: 1.0}
G_ABSOLUTE = 90
G_INCREMENTAL = 91
G_PLANE_XY = 17
PLANES = {
    17: ((0, 1, 2), ("I", "J")),   # XY, normal Z
    18: ((2, 0, 1), ("K", "I")),   # ZX, normal Y
    19: ((1, 2, 0), ("J", "K")),   # YZ, normal X
}
G_SET_POSITION = 92
G_NOT_SIMULATED = {10, 28, 30, 53}  # usam X/Y/Z, mas não como destino de corte
G_IGNORED = {40, 41, 42, 43, 49, 54, 55, 56, 57, 58, 59, 61, 64, 94}
G_CYCLE_CANCEL = 80
G_RETURN_INITIAL = 98  # ciclo recua ao nível em que começou
G_RETURN_R = 99        # ciclo recua só até o plano R
CYCLE_WORDS = "ZRQP"   # parâmetros que o ciclo guarda de uma linha para a outra
MOTION_ARCS = (G_CW_ARC, G_CCW_ARC)
AXES = "XYZ"
BOUNDS_TOLERANCE = 1e-6
TWO_PI = 2 * math.pi
MIN_CHORD = 1e-9          # mm; abaixo disso início e fim do arco são o mesmo ponto
RADIUS_TOLERANCE = 1e-3   # folga para o arredondamento do pós-processador (0,1% do raio)

__all__ = [
    "ERROR", "WARNING", "Issue", "Move", "ParseResult", "arc_points",
    "clean_line", "parse_gcode", "parse_words",
]


@dataclass(frozen=True)
class Move:
    """um trecho de movimento. arcos viram vários Move; G04 vira um Move de espera."""
    start: Point
    end: Point
    is_cut: bool
    feed: float        # mm/min programado; relevante apenas para cortes
    line: int = 0      # linha de origem no arquivo, começando em 1
    active: bool = False  # processo ligado (spindle, arco, tocha) durante o movimento
    dwell: float = 0.0    # segundos de espera (G04); quando > 0, start == end
    rapid: bool = False   # G0: deslocamento rápido, na velocidade de avanço rápido

    @property
    def length(self) -> float:
        return math.dist(self.start, self.end)


@dataclass(frozen=True)
class ParseResult:
    moves: list[Move] = field(default_factory=list)
    issues: list[Issue] = field(default_factory=list)
    commands: dict[str, int] = field(default_factory=dict)  # G0 a G4 executados


def parse_gcode(text: str, default_feed: float = DEFAULT_FEED,
                limits: Limits = MACHINE_LIMITS,
                dialect: Dialect | None = None,
                arc_step_deg: float = ARC_STEP_DEG) -> ParseResult:
    """expande o programa e interpreta a sequência resultante."""
    dialect = dialect or get_dialect(DEFAULT_DIALECT)
    expansion = expand_program(text)

    interpreter = GCodeInterpreter(default_feed, limits, dialect, arc_step_deg)
    for source in expansion.lines:
        interpreter.run_line(source.text, source.line)

    issues = sorted([*expansion.issues, *interpreter.issues], key=lambda issue: issue.line)
    return ParseResult(
        moves=interpreter.moves,
        issues=issues,
        commands=interpreter.commands,
    )


def arc_points(start: Point, end: Point, center: tuple[float, float],
               clockwise: bool, step_deg: float = ARC_STEP_DEG) -> list[Point]:
    """pontos de um arco nas duas primeiras coordenadas; a terceira varia linearmente (hélice)."""
    cx, cy = center
    radius = math.hypot(start[0] - cx, start[1] - cy)
    a_start = math.atan2(start[1] - cy, start[0] - cx)
    a_end = math.atan2(end[1] - cy, end[0] - cx)
    sweep = _signed_sweep(a_end - a_start, clockwise)

    steps = max(1, math.ceil(abs(sweep) / math.radians(step_deg)))
    points: list[Point] = []
    for i in range(1, steps + 1):
        t = i / steps
        angle = a_start + sweep * t
        z = start[2] + (end[2] - start[2]) * t
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle), z))

    points[-1] = end  # o último ponto é exatamente o destino
    return points

def center_from_radius(start: Point, end: Point, radius: float,
                       clockwise: bool) -> tuple[float, float]:
    """centro de um arco programado com R. R positivo é o arco de até 180°; negativo, o maior."""
    dx, dy = end[0] - start[0], end[1] - start[1]
    chord = math.hypot(dx, dy)
    if chord < MIN_CHORD:
        raise GCodeError(tr("issue_arc_r_full_circle"))
    half = chord / 2
    if half > abs(radius) * (1 + RADIUS_TOLERANCE):
        raise GCodeError(tr("issue_arc_r_too_small").format(radius=abs(radius), needed=half))
    height = math.sqrt(max(0.0, radius * radius - half * half))
    # o centro fica à esquerda da corda no G3 e à direita no G2; R negativo inverte o lado
    side = 1.0 if clockwise == (radius < 0) else -1.0
    middle_x, middle_y = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
    return (middle_x - side * height * dy / chord, middle_y + side * height * dx / chord)

def _from_plane(point: Point, axes: tuple[int, int, int]) -> Point:
    """devolve um ponto (u, v, normal) do plano ativo para (X, Y, Z)."""
    xyz = [0.0, 0.0, 0.0]
    for value, axis in zip(point, axes):
        xyz[axis] = value
    return (xyz[0], xyz[1], xyz[2])

def _signed_sweep(delta: float, clockwise: bool) -> float:
    """ajusta o ângulo varrido para o sentido pedido pelo G2 ou G3."""
    if clockwise and delta >= 0:
        return delta - TWO_PI
    if not clockwise and delta <= 0:
        return delta + TWO_PI
    return delta


class GCodeInterpreter:
    """mantém o estado modal da máquina enquanto percorre as linhas expandidas."""

    def __init__(self, default_feed: float, limits: Limits = MACHINE_LIMITS,
                 dialect: Dialect | None = None, arc_step_deg: float = ARC_STEP_DEG) -> None:
        self.position: Point = (0.0, 0.0, 0.0)
        self.absolute = True
        self.unit_scale = 1.0
        self.motion = G_RAPID
        self.feed = default_feed
        self.limits = limits
        self.dialect = dialect or get_dialect(DEFAULT_DIALECT)
        self.arc_step_deg = arc_step_deg
        self.process_active = False
        self.moves: list[Move] = []
        self.issues: list[Issue] = []
        self.commands = {"G0": 0, "G1": 0, "G2": 0, "G3": 0, "G4": 0}
        self.plane = G_PLANE_XY
        self.offset = [0.0, 0.0, 0.0]  # deslocamento do G92, por eixo
        self._unknown_warned: set[int] = set()
        self.cycle: int | None = None        # ciclo de furação ativo (G73/G81/G82/G83)
        self.cycle_words: dict[str, float] = {}
        self.cycle_initial_z = 0.0
        self.return_to_r = False             # G99; o padrão (G98) volta ao nível inicial

        self._lineno = 0
        self._feed_programmed = False
        self._feed_warned = False
        self._bounds_reported_line = 0
        self._overflow = False  # passou de MAX_MOVES: as linhas seguintes são ignoradas

    def run_line(self, line: str, lineno: int) -> None:
        self._lineno = lineno
        if self._overflow:
            return
        try:
            self._execute(line)
        except GCodeError as err:
            self._report(ERROR, str(err))

    # --- interpretação da linha ---

    def _execute(self, line: str) -> None:
        words = parse_words(line)
        if not words:
            return

        g_codes = [int(value) for letter, value in words if letter == "G"]
        m_codes = [int(value) for letter, value in words if letter == "M"]
        params = {letter: value for letter, value in words if letter not in "GM"}

        # G e M são aplicados primeiro, na ordem em que aparecem na linha
        for code in g_codes:
            self._apply_g_code(code)
        for code in m_codes:
            self._apply_m_code(code)

        if "F" in params:
            self.feed = params["F"] * self.unit_scale
            self._feed_programmed = True

        if G_DWELL in g_codes:
            self._dwell(self._dwell_seconds(params))
            return  # na linha do G04, X e U são tempo de espera, nunca coordenada

        if G_SET_POSITION in g_codes:
            self._set_position(params)
            return
        skipped = [code for code in g_codes if code in G_NOT_SIMULATED]
        if skipped:
            self._report(WARNING, tr("issue_g_not_simulated").format(code=skipped[0]))
            return

        if self.cycle is not None:
            self._drill(params)
        elif any(axis in params for axis in AXES):
            self._move(params)

    def _apply_g_code(self, code: int) -> None:
        if code in (G_RAPID, G_LINEAR, *MOTION_ARCS):
            self.motion = code
            self.cycle = None  # um movimento comum encerra o ciclo
        elif code in DRILL_CYCLES:
            if self.cycle is None:
                self.cycle_initial_z = self.position[2]
                self.cycle_words = {}
            self.cycle = code
        elif code == G_CYCLE_CANCEL:
            self.cycle = None
        elif code in (G_RETURN_INITIAL, G_RETURN_R):
            self.return_to_r = code == G_RETURN_R
        elif code in G_UNITS:
            self.unit_scale = G_UNITS[code]
        elif code == G_ABSOLUTE:
            self.absolute = True
        elif code == G_INCREMENTAL:
            self.absolute = False
        elif code in PLANES:
            self.plane = code
        elif code not in (G_DWELL, G_SET_POSITION, *G_NOT_SIMULATED, *G_IGNORED) \
                and code not in self._unknown_warned:
            self._unknown_warned.add(code)
            self._report(WARNING, tr("issue_g_unknown").format(code=code))

    def _apply_m_code(self, code: int) -> None:
        """M-codes de processo são definidos pelo dialeto; os demais são ignorados."""
        if code in self.dialect.process_on:
            self.process_active = True
        elif code in self.dialect.process_off:
            self.process_active = False

    def _move(self, words: dict[str, float]) -> None:
        self.commands[f"G{self.motion}"] += 1
        end = self._target(words)
        if self.motion in MOTION_ARCS:
            self._arc(end, words)
        else:
            self._line(end)
        self.position = end

    def _target(self, words: dict[str, float]) -> Point:
        def resolve(i: int, axis: str) -> float:
            current = self.position[i]
            if axis not in words:
                return current
            value = words[axis] * self.unit_scale
            return value + self.offset[i] if self.absolute else current + value

        return (resolve(0, "X"), resolve(1, "Y"), resolve(2, "Z"))

    # --- ciclos de furação ---

    def _drill(self, words: dict[str, float]) -> None:
        """no ciclo, Z é a profundidade e R o plano de aproximação; cada X/Y é um furo."""
        self.cycle_words.update({k: v for k, v in words.items() if k in CYCLE_WORDS})
        if "X" not in words and "Y" not in words:
            return  # a linha só ajusta parâmetros; o furo sai quando vier uma posição
        if "Z" not in self.cycle_words or "R" not in self.cycle_words:
            raise GCodeError(tr("issue_cycle_missing_zr").format(code=self.cycle))

        r_level, bottom = self._cycle_levels()
        retract = r_level if self.return_to_r else max(self.cycle_initial_z, r_level)
        peck = abs(self.cycle_words.get("Q", 0.0)) * self.unit_scale
        steps = drill_steps(self.cycle, r_level, bottom, retract, peck)

        x, y, _ = self._target({k: v for k, v in words.items() if k in "XY"})
        self._check_feed()
        self._check_bounds([(x, y, z) for z in (self.position[2], r_level, bottom, retract)])
        name = f"G{self.cycle}"
        self.commands[name] = self.commands.get(name, 0) + 1

        self._cycle_segment((x, y, self.position[2]), rapid=True)
        for step in steps:
            if step.kind == DWELL:
                seconds = self.cycle_words.get("P", 0.0) * self.dialect.dwell_unit
                if seconds > 0:
                    self._add_move(Move(self.position, self.position, False, self.feed, self._lineno,
                                        active=self.process_active, dwell=seconds))
            else:
                self._cycle_segment((x, y, step.z), rapid=step.kind == RAPID)

    def _cycle_levels(self) -> tuple[float, float]:
        """(plano R, fundo) em coordenadas de máquina. em G91, R conta do nível inicial e Z, do R."""
        r = self.cycle_words["R"] * self.unit_scale
        z = self.cycle_words["Z"] * self.unit_scale
        if self.absolute:
            return r + self.offset[2], z + self.offset[2]
        r_level = self.cycle_initial_z + r
        return r_level, r_level + z

    def _cycle_segment(self, end: Point, rapid: bool) -> None:
        if end == self.position:
            return
        self._add_move(Move(self.position, end, not rapid, self.feed, self._lineno,
                            active=self.process_active, rapid=rapid))
        self.position = end

    def _set_position(self, words: dict[str, float]) -> None:
        """G92: a posição atual passa a valer o que a linha diz, sem mover a ferramenta."""
        for i, axis in enumerate(AXES):
            if axis in words:
                self.offset[i] = self.position[i] - words[axis] * self.unit_scale

    # --- movimentos e esperas ---

    def _add_move(self, move: Move) -> None:
        """único ponto de entrada de movimentos, para o limite valer em retas, arcos e esperas."""
        if len(self.moves) >= MAX_MOVES:
            self._overflow = True
            raise GCodeError(tr("issue_too_many_moves").format(max_moves=MAX_MOVES))
        self.moves.append(move)

    def _dwell_seconds(self, params: dict[str, float]) -> float:
        """tempo do G04: P na unidade do dialeto; X ou U sempre em segundos."""
        if "P" in params:
            return params["P"] * self.dialect.dwell_unit
        for letter in DWELL_SECONDS_WORDS:
            if letter in params:
                return params[letter]
        self._report(WARNING, tr("issue_dwell_without_time"))
        return 0.0

    def _dwell(self, seconds: float) -> None:
        """G04: espera no mesmo ponto."""
        if seconds <= 0:
            return
        self.commands["G4"] += 1
        self._add_move(Move(
            start=self.position,
            end=self.position,
            is_cut=False,
            feed=self.feed,
            line=self._lineno,
            active=self.process_active,
            dwell=seconds,
        ))

    def _line(self, end: Point) -> None:
        if end == self.position:
            return
        is_cut = self.motion != G_RAPID
        if is_cut:
            self._check_feed()
        self._check_bounds([end])
        self._add_move(Move(
            self.position, end, is_cut, self.feed, self._lineno,
            active=self.process_active,
            rapid=self.motion == G_RAPID,
        ))

    def _arc(self, end: Point, words: dict[str, float]) -> None:
        axes, (center_u, center_v) = PLANES[self.plane]
        start = self.position
        # o arco é calculado no plano ativo (u, v) e devolvido em X, Y, Z
        plane_start = tuple(start[i] for i in axes)
        plane_end = tuple(end[i] for i in axes)
        clockwise = self.motion == G_CW_ARC
        if "R" in words:  # quando R e o centro aparecem juntos, vale o R, como nos controladores
            center = center_from_radius(plane_start, plane_end, words["R"] * self.unit_scale, clockwise)
        elif center_u in words or center_v in words:
            center = (
                plane_start[0] + words.get(center_u, 0.0) * self.unit_scale,
                plane_start[1] + words.get(center_v, 0.0) * self.unit_scale,
            )
        else:
            raise GCodeError(tr("issue_arc_missing_center").format(letters="/".join(sorted((center_u, center_v)))))

        self._check_feed()
        points = [
            _from_plane(point, axes)
            for point in arc_points(plane_start, plane_end, center, clockwise=clockwise,
                                    step_deg=self.arc_step_deg)
        ]
        self._check_bounds(points)

        previous = start
        for point in points:
            self._add_move(Move(
                previous, point, True, self.feed, self._lineno,
                active=self.process_active,
            ))
            previous = point

    # --- validação ---

    def _check_feed(self) -> None:
        """avisa uma única vez se o corte começa sem F programado."""
        if self._feed_programmed or self._feed_warned:
            return
        self._feed_warned = True
        self._report(WARNING, tr("issue_feed_missing").format(feed=f"{self.feed:g}"))

    def _check_bounds(self, points: list[Point]) -> None:
        """reporta no máximo um problema de área de trabalho por linha."""
        if self._bounds_reported_line == self._lineno:
            return
        for point in points:
            for axis, value in zip(AXES, point):
                low, high = self.limits[axis]
                if not low - BOUNDS_TOLERANCE <= value <= high + BOUNDS_TOLERANCE:
                    self._bounds_reported_line = self._lineno
                    self._report(
                        ERROR,
                        tr("issue_out_of_bounds").format(
                            axis=axis, value=f"{value:.2f}", low=f"{low:g}", high=f"{high:g}",
                        ),
                    )
                    return

    def _report(self, severity: str, message: str) -> None:
        self.issues.append(Issue(self._lineno, severity, message))