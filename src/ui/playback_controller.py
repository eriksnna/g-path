"""relógio da reprodução: liga o modelo Playback a um timer e avisa a tela a cada mudança."""
from __future__ import annotations

from PySide6.QtCore import QElapsedTimer, QObject, QTimer, Signal

from config import TICK_MS
from core.playback import Playback
from core.timeline import TimelineMarks, step_layer, step_move
from core.toolpath import Toolpath


class PlaybackController(QObject):
    changed = Signal()  # tempo, velocidade ou play/pause mudaram; a tela deve se redesenhar

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._model = Playback()
        self._toolpath: Toolpath | None = None
        self._marks = TimelineMarks()
        self._timer = QTimer(self)
        self._timer.setInterval(TICK_MS)
        self._timer.timeout.connect(self._on_tick)
        self._clock = QElapsedTimer()

    # --- leitura do estado ---

    @property
    def elapsed(self) -> float:
        return self._model.elapsed

    @property
    def progress(self) -> float:
        return self._model.progress

    @property
    def playing(self) -> bool:
        return self._model.playing

    @property
    def speed(self) -> float:
        return self._model.speed

    # --- comandos ---

    def load(self, toolpath: Toolpath, marks: TimelineMarks) -> None:
        """prepara um novo percurso. não avisa a tela: quem carrega redesenha quando terminar."""
        self._toolpath = toolpath
        self._marks = marks
        self._model.reset(toolpath.total_time)

    def toggle(self) -> None:
        self._model.toggle()
        self._changed()

    def pause(self) -> None:
        self._model.pause()
        self._timer.stop()
        self._changed()

    def seek(self, seconds: float) -> None:
        """pausa e vai a um instante (ex.: ao clicar em um problema da validação)."""
        self._model.pause()
        self._model.seek(seconds)
        self._changed()

    def go_to_start(self) -> None:
        self.seek(0.0)

    def go_to_end(self) -> None:
        self.seek(self._model.total_time)

    def step(self, direction: int, by_layer: bool = False) -> None:
        """pula um movimento ou, com by_layer, uma camada inteira."""
        if self._toolpath is None:
            return
        t = self._model.elapsed
        if by_layer and self._marks.layer_starts.size:
            target = step_layer(self._marks, t, direction)
        else:
            target = step_move(self._toolpath, t, direction)
        self.seek(target)

    def scrub(self, fraction: float) -> None:
        self._model.seek_fraction(fraction)
        self._changed()

    def set_speed(self, value: float) -> None:
        self._model.set_speed(value)
        self._changed()

    # --- relógio ---

    def _on_tick(self) -> None:
        seconds = self._clock.restart() / 1000.0
        self._model.advance(seconds)
        self._changed()

    def _changed(self) -> None:
        if self._model.playing and not self._timer.isActive():
            self._clock.start()
            self._timer.start()
        elif not self._model.playing and self._timer.isActive():
            self._timer.stop()
        self.changed.emit()