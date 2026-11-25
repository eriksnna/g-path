"""sugestão de outro dialeto quando o arquivo usa códigos de processo que o perfil não reconhece."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSettings

from core.dialect import Dialect, dialect_label, get_dialect, process_codes_label, suggest_dialect
from core.i18n import tr
from ui.suggestion_banner import SuggestionBanner

MAX_DISMISSED_SUGGESTIONS = 50
DISMISSED_KEY = "suggestions/dismissed"


class DialectSuggestion:
    """decide quando mostrar a faixa e lembra, por arquivo, as sugestões dispensadas.
    aceitar a sugestão continua com a janela, que é quem troca o dialeto do perfil."""

    def __init__(self, banner: SuggestionBanner, settings: QSettings) -> None:
        self._banner = banner
        self._settings = settings
        self._path: Path | None = None
        banner.dismissed.connect(self._dismiss)

    def update(self, text: str, path: Path | None, current_key: str, current: Dialect) -> None:
        self._path = path
        key = suggest_dialect(text, current)
        if key is None or self._dismissal_id(key) in self._dismissed():
            self._banner.hide()
            return
        self._banner.show_suggestion(
            key,
            tr("dialect_suggestion").format(
                codes=process_codes_label(get_dialect(key)), current=dialect_label(current_key)),
            tr("dialect_suggestion_action").format(name=dialect_label(key)),
        )

    def _dismissal_id(self, key: str) -> str:
        """identifica a sugestão por arquivo: dispensar em um não cala nos outros."""
        return f"{self._path or ''}|{key}"

    def _dismissed(self) -> list[str]:
        value = self._settings.value(DISMISSED_KEY, [])
        if isinstance(value, str):  # QSettings devolve string quando sobra só 1 item salvo
            value = [value]
        return list(value or [])

    def _dismiss(self, key: str) -> None:
        """o × vale para este arquivo, e continua valendo nas próximas aberturas."""
        dismissed = self._dismissed()
        dismissed.insert(0, self._dismissal_id(key))
        self._settings.setValue(DISMISSED_KEY, dismissed[:MAX_DISMISSED_SUGGESTIONS])