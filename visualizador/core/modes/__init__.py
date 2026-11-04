"""Modos de processo disponíveis e fábrica para criá-los."""
from __future__ import annotations

from core.i18n import tr
from core.modes.base import ModeCard, ProcessMode, apply_mode
from core.modes.deposition import BeadSpec, DepositionMode
from core.modes.machining import MachiningMode

# Chave i18n do nome exibido de cada modo. MachiningMode.name/DepositionMode.name
# continuam existindo (usados como identificador "canônico", nunca mostrados
# direto na tela) — quem monta um combo/rótulo pro usuário usa mode_choices()
# ou mode_display_name() abaixo, que traduzem na hora da chamada (não na
# importação do módulo, que aconteceria antes do idioma salvo ser carregado).

_MODE_LABEL_KEYS = {
    MachiningMode.key: "mode_machining_name",
    DepositionMode.key: "mode_deposition_name",
}


def mode_display_name(key: str) -> str:
    return tr(_MODE_LABEL_KEYS.get(key, key))


def mode_choices() -> list[tuple[str, str]]:
    return [(mode_display_name(cls.key), cls.key) for cls in (MachiningMode, DepositionMode)]


MODE_CHOICES = mode_choices()


def create_mode(key: str, bead: BeadSpec) -> ProcessMode:
    if key == MachiningMode.key:
        return MachiningMode()
    if key == DepositionMode.key:
        return DepositionMode(bead)
    raise ValueError(f"modo desconhecido: {key!r}")


__all__ = [
    "BeadSpec", "MODE_CHOICES", "ModeCard", "ProcessMode", "apply_mode",
    "create_mode", "mode_choices", "mode_display_name",
]