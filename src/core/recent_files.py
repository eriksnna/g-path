"""arquivos abertos recentemente e o último aberto. guarda num QSettings, mas não depende de Qt:
qualquer objeto com value, setValue e remove serve (os testes usam um dicionário)."""
from __future__ import annotations

from pathlib import Path

from config import MAX_RECENT_FILES

RECENT_KEY = "window/recent_files"
LAST_KEY = "window/last_file"


class RecentFiles:
    def __init__(self, settings) -> None:
        self._settings = settings

    def existing(self) -> list[str]:
        """recentes que ainda existem no disco, do mais novo ao mais antigo."""
        return [p for p in self._stored() if Path(p).exists()]

    def opened(self, path: Path) -> None:
        """registra um arquivo aberto: vai para o topo da lista e vira o último aberto."""
        recent = [p for p in self._stored() if p != str(path)]
        recent.insert(0, str(path))
        self._settings.setValue(RECENT_KEY, recent[:MAX_RECENT_FILES])
        self._settings.setValue(LAST_KEY, str(path))

    def last_file(self) -> Path | None:
        """o último arquivo aberto, se ainda existir; reaberto ao iniciar o programa."""
        value = self._settings.value(LAST_KEY)
        if not value:
            return None
        path = Path(str(value))
        return path if path.exists() else None

    def forget_last(self) -> None:
        self._settings.remove(LAST_KEY)

    def _stored(self) -> list[str]:
        value = self._settings.value(RECENT_KEY, [])
        if isinstance(value, str):  # QSettings devolve string quando sobra só 1 item salvo
            value = [value]
        return [str(p) for p in value or []]