"""persistência dos perfis de máquina em disco (JSON na pasta de configuração do usuário).

falha ao ler ou escrever esse arquivo nunca deve travar o app: persistência é uma
conveniência, então qualquer problema (arquivo corrompido, sem permissão de escrita,
ou um arquivo salvo por uma versão anterior sem os campos "mode"/"dialect") cai de
volta em padrões, silenciosamente.
"""
import json
import math

import config
from core.dialect import DIALECTS
from core.machine_profile import DEFAULT_LIMITS, MachineProfile, default_profiles
from core.modes import mode_choices

MAX_NAME_LENGTH = 80
COORD_LIMIT = 1_000_000.0      # mesma faixa dos campos da tela de ajustes
FEED_RANGE = (0.1, 100_000.0)
ARC_STEP_RANGE = (0.1, 45.0)


def _number(value, default: float, low: float, high: float) -> float:
    """float dentro da faixa; NaN, infinito, texto ou valor fora dela viram o padrão."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) and low <= number <= high else default


def _limits(raw) -> dict[str, tuple[float, float]]:
    limits = dict(DEFAULT_LIMITS)
    for axis, default in DEFAULT_LIMITS.items():
        try:
            low = _number(raw[axis][0], default[0], -COORD_LIMIT, COORD_LIMIT)
            high = _number(raw[axis][1], default[1], -COORD_LIMIT, COORD_LIMIT)
        except (KeyError, IndexError, TypeError):
            continue
        if low <= high:
            limits[axis] = (low, high)
    return limits


def _known(value, valid, default: str) -> str:
    return value if value in valid else default


def load_profiles() -> tuple[list[MachineProfile], str | None]:
    """carrega perfis salvos e o nome do perfil ativo. sem arquivo ou corrompido -> padrões."""
    if not config.PROFILES_FILE.exists():
        return default_profiles(), None
    try:
        data = json.loads(config.PROFILES_FILE.read_text(encoding="utf-8"))
        modes = {key for _, key in mode_choices()}
        profiles = [
            MachineProfile(
                name=str(item["name"])[:MAX_NAME_LENGTH],
                limits=_limits(item.get("limits")),
                mode_key=_known(item.get("mode"), modes, config.DEFAULT_MODE),
                dialect_key=_known(item.get("dialect"), DIALECTS, config.DEFAULT_DIALECT),
                rapid_feed=_number(item.get("rapid_feed"), config.RAPID_FEED, *FEED_RANGE),
                default_feed=_number(item.get("default_feed"), config.DEFAULT_FEED, *FEED_RANGE),
                min_feed=_number(item.get("min_feed"), config.MIN_FEED, *FEED_RANGE),
                arc_step_deg=_number(item.get("arc_step_deg"), config.ARC_STEP_DEG, *ARC_STEP_RANGE),
            )
            for item in data["profiles"]
        ]
        if not profiles:
            return default_profiles(), None
        return profiles, data.get("active")
    except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError):
        return default_profiles(), None


def save_profiles(profiles: list[MachineProfile], active_name: str) -> None:
    """salva perfis e qual está ativo. erros de escrita são ignorados silenciosamente."""
    payload = {
        "active": active_name,
        "profiles": [
            {
                "name": p.name,
                "limits": {axis: list(bounds) for axis, bounds in p.limits.items()},
                "mode": p.mode_key,
                "dialect": p.dialect_key,
                "rapid_feed": p.rapid_feed,
                "default_feed": p.default_feed,
                "min_feed": p.min_feed,
                "arc_step_deg": p.arc_step_deg,
            }
            for p in profiles
        ],
    }
    try:
        config.PROFILES_FILE.parent.mkdir(parents=True, exist_ok=True)
        config.PROFILES_FILE.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    except OSError:
        pass