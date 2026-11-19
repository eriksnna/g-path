"""avisa quando outro programa altera o arquivo aberto."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QFileSystemWatcher, QObject, QTimer, Signal

DISK_RELOAD_DELAY_MS = 400  # espera o outro programa terminar de gravar


class FileWatcher(QObject):
    changed = Signal()  # o arquivo vigiado mudou no disco (avisos seguidos viram um só)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._watcher = QFileSystemWatcher(self)
        self._delay = QTimer(self)
        self._delay.setSingleShot(True)
        self._delay.setInterval(DISK_RELOAD_DELAY_MS)
        self._delay.timeout.connect(self.changed.emit)
        self._watcher.fileChanged.connect(lambda _path: self._delay.start())

    def watch(self, path: Path | None) -> None:
        """passa a vigiar só este arquivo (ou nenhum). chame de novo depois de cada aviso:
        quem regrava o arquivo por substituição faz o sistema soltar a vigilância."""
        watched = self._watcher.files()
        if watched:
            self._watcher.removePaths(watched)
        if path is not None:
            self._watcher.addPath(str(path))