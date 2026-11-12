"""barra de reprodução. exibe o estado e emite sinais; não decide nada sozinha."""
from __future__ import annotations

import math

from html import escape

from core.i18n import tr
from contextlib import contextmanager

from PySide6.QtCore import QPointF, QRectF, QSize, Qt, Signal, QEasingCurve, QPropertyAnimation, QTimer
from PySide6.QtGui import QAction, QColor, QPainter
from PySide6.QtWidgets import (
    QFrame, QGridLayout, QHBoxLayout, QLabel, QMenu, QPushButton, QSizePolicy, QSlider,
    QToolButton, QVBoxLayout, QWidget, QWidgetAction,
)

from config import (
    SPEED_MAX, SPEED_MIN, SPEED_PRESETS, SPEED_SLIDER_SCALE, TIMELINE_STEPS,
)
from core.stats import format_duration
from core.timeline import TimelineMarks
from ui.theme import ( 
    ACCENT, ACCENT_TEXT, SPACE_XXS, SPACE_MD, SPACE_SM, SPACE_XL, BORDER_STRONG,
    TEXT_MUTED, ON_ACCENT, SPACE_LG
)
from ui.icons import FAST_FORWARD, PAUSE, PLAY, REWIND, SKIP_BACK, SKIP_FORWARD, icon

PLAY_BUTTON_SIZE = (40, 40)
TRANSPORT_BUTTON_SIZE = (34, 34)
SPEED_SLIDER_WIDTH = 180
MESSAGE_TIMEOUT_MS = 4000
LINE_CHIP_MAX_CHARS = 28

@contextmanager
def _signals_blocked(widget):
    """atualiza um widget por código sem disparar seus sinais."""
    previous = widget.blockSignals(True)
    try:
        yield
    finally:
        widget.blockSignals(previous)

class _Slider(QSlider):
    TRACK_HEIGHT = 6
    HANDLE_RADIUS = 8

    def _track_rect(self) -> QRectF:
        return QRectF(
            self.HANDLE_RADIUS, self.height() / 2 - self.TRACK_HEIGHT / 2,
            self.width() - 2 * self.HANDLE_RADIUS, self.TRACK_HEIGHT,
        )

    def _fraction(self) -> float:
        span = max(self.maximum() - self.minimum(), 1)
        return (self.value() - self.minimum()) / span

    def _fraction_from_x(self, x: float) -> float:
        track = self._track_rect()
        return min(max((x - track.left()) / max(track.width(), 1), 0.0), 1.0)

    def _value_from_x(self, x: float) -> int:
        return round(self.minimum() + self._fraction_from_x(x) * (self.maximum() - self.minimum()))

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        track = self._track_rect()
        radius = self.TRACK_HEIGHT / 2

        painter.setBrush(QColor(BORDER_STRONG))
        painter.drawRoundedRect(track, radius, radius)
        self._paint_under_handle(painter, track)

        fraction = self._fraction()
        handle_x = track.left() + fraction * track.width()
        if fraction > 0:
            filled = QRectF(track.left(), track.top(), handle_x - track.left(), self.TRACK_HEIGHT)
            painter.setBrush(QColor(ACCENT if self.isEnabled() else TEXT_MUTED))
            painter.drawRoundedRect(filled, radius, radius)

        painter.setBrush(QColor("#ffffff" if self.isEnabled() else TEXT_MUTED))
        painter.drawEllipse(QPointF(handle_x, track.center().y()), self.HANDLE_RADIUS, self.HANDLE_RADIUS)
        painter.end()

    def _paint_under_handle(self, painter: QPainter, track: QRectF) -> None:
        """gancho para subclasses desenharem marcas entre o trilho e o cursor."""

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton and self.isEnabled():
            self.setValue(self._value_from_x(event.position().x()))
            self.sliderPressed.emit()
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if event.buttons() & Qt.MouseButton.LeftButton and self.isEnabled():
            self.setValue(self._value_from_x(event.position().x()))
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.sliderReleased.emit()
            event.accept()
        else:
            super().mouseReleaseEvent(event)

class _HoverGrowButton(QPushButton):
    GROW_FACTOR = 1.12

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._base_icon_size: QSize | None = None
        self._icon_animation = QPropertyAnimation(self, b"iconSize", self)
        self._icon_animation.setDuration(100)
        self._icon_animation.setEasingCurve(QEasingCurve.Type.OutQuad)

    def setIconSize(self, size: QSize) -> None:
        super().setIconSize(size)
        if self._base_icon_size is None:
            self._base_icon_size = size

    def enterEvent(self, event) -> None:
        super().enterEvent(event)
        self._animate_to(self._base_icon_size * self.GROW_FACTOR if self.isEnabled() else self._base_icon_size)

    def leaveEvent(self, event) -> None:
        super().leaveEvent(event)
        self._animate_to(self._base_icon_size)

    def _animate_to(self, target: QSize | None) -> None:
        if target is None:
            return
        self._icon_animation.stop()
        self._icon_animation.setStartValue(self.iconSize())
        self._icon_animation.setEndValue(target)
        self._icon_animation.start()

class PlayerBar(QFrame):
    play_clicked = Signal()
    start_clicked = Signal()
    end_clicked = Signal()
    step_clicked = Signal(int)     # -1 ou 1
    scrub_started = Signal()
    scrubbed = Signal(float)       # fração de 0 a 1
    speed_changed = Signal(float)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("playbar")

        self._timeline = _Slider(Qt.Orientation.Horizontal)
        self._timeline.setRange(0, TIMELINE_STEPS)
        self._timeline.sliderPressed.connect(self.scrub_started.emit)
        self._timeline.valueChanged.connect(
            lambda value: self.scrubbed.emit(value / TIMELINE_STEPS)
        )

        self._play_button = self._make_button(
            icon(PLAY, ON_ACCENT), tr("tooltip_play_pause"), self.play_clicked.emit, PLAY_BUTTON_SIZE, name="play",
        )
        self._transport = [
            self._make_button(icon(SKIP_BACK), tr("tooltip_go_start"), self.start_clicked.emit, TRANSPORT_BUTTON_SIZE, name="transport"),
            self._make_button(icon(REWIND), tr("tooltip_step_back"), lambda: self.step_clicked.emit(-1), TRANSPORT_BUTTON_SIZE, name="transport"),
            self._play_button,
            self._make_button(icon(FAST_FORWARD), tr("tooltip_step_forward"), lambda: self.step_clicked.emit(1), TRANSPORT_BUTTON_SIZE, name="transport"),
            self._make_button(icon(SKIP_FORWARD), tr("tooltip_go_end"), self.end_clicked.emit, TRANSPORT_BUTTON_SIZE, name="transport"),
        ]

        self._elapsed_label = self._make_time_label("timeLabel")
        self._elapsed_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self._total_label = self._make_time_label("timeLabelMuted")

        self._speed_slider = _Slider(Qt.Orientation.Horizontal)
        self._speed_slider.setRange(
            round(SPEED_MIN * SPEED_SLIDER_SCALE), round(SPEED_MAX * SPEED_SLIDER_SCALE),
        )
        self._speed_slider.setFixedWidth(SPEED_SLIDER_WIDTH)
        self._speed_slider.valueChanged.connect(self._on_speed_slider)
        self._speed_actions: list[tuple[float, QAction]] = []
        self._speed_button = self._make_speed_button()

        self._message = QLabel()
        self._line_chip = self._make_chip()
        self._layer_chip = self._make_chip()
        self._layer_total = 0
        self._chips_allowed = True
        self._message = QLabel()
        self._message.setObjectName("playerMessage")
        self._message_timer = QTimer(self)
        self._message_timer.setSingleShot(True)
        self._message_timer.timeout.connect(lambda: self.set_status(""))

        self._controls = [*self._transport, self._timeline, self._speed_button]
        self._build_layout()

    # --- montagem ---

    def _build_layout(self) -> None:
        timeline_row = QHBoxLayout()
        timeline_row.setSpacing(SPACE_LG)
        timeline_row.addWidget(self._elapsed_label)
        timeline_row.addWidget(self._timeline, 1)
        timeline_row.addWidget(self._total_label)

        transport = QHBoxLayout()
        transport.setSpacing(SPACE_XXS)
        for widget in self._transport:
            transport.addWidget(widget)

        # colunas laterais com o mesmo stretch mantêm o transporte no centro real
        controls_row = QGridLayout()
        info = QWidget()
        # não deixa chips ou mensagem longa empurrarem o transporte para fora do centro
        info.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        info_layout = QHBoxLayout(info)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(SPACE_SM)
        info_layout.addWidget(self._line_chip)
        info_layout.addWidget(self._layer_chip)
        info_layout.addWidget(self._message)
        info_layout.addStretch()

        controls_row = QGridLayout()
        controls_row.addWidget(info, 0, 0)
        controls_row.addLayout(transport, 0, 1)
        controls_row.addWidget(self._speed_button, 0, 2,
                               Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        controls_row.setColumnStretch(0, 1)
        controls_row.setColumnStretch(2, 1)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACE_XL, SPACE_MD, SPACE_XL, SPACE_MD)
        layout.setSpacing(SPACE_SM)
        layout.addLayout(timeline_row)
        layout.addLayout(controls_row)

    def _make_speed_button(self) -> QToolButton:
        button = QToolButton()
        button.setObjectName("speedButton")
        button.setToolTip(tr("label_speed"))
        button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        menu = QMenu(button)
        for value in SPEED_PRESETS:
            action = menu.addAction(f"{value:g}x")
            action.setCheckable(True)
            action.triggered.connect(lambda _checked=False, v=value: self.speed_changed.emit(v))
            self._speed_actions.append((value, action))
        menu.addSeparator()

        holder = QWidget()
        holder_layout = QHBoxLayout(holder)
        holder_layout.setContentsMargins(SPACE_MD, SPACE_SM, SPACE_MD, SPACE_SM)
        holder_layout.addWidget(self._speed_slider)
        slider_action = QWidgetAction(menu)
        slider_action.setDefaultWidget(holder)
        menu.addAction(slider_action)

        button.setMenu(menu)
        return button

    @staticmethod
    def _make_chip() -> QLabel:
        chip = QLabel()
        chip.setObjectName("chip")
        chip.setTextFormat(Qt.TextFormat.RichText)
        chip.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        chip.setVisible(False)
        return chip

    @staticmethod
    def _make_time_label(object_name: str) -> QLabel:
        label = QLabel("00:00")
        label.setObjectName(object_name)
        return label

    def _on_speed_slider(self, units: int) -> None:
        self.speed_changed.emit(units / SPEED_SLIDER_SCALE)

    # --- estado exibido (não emite sinais) ---

    def set_enabled(self, enabled: bool) -> None:
        for widget in self._controls:
            widget.setEnabled(enabled)
        if not enabled:
            self._elapsed_label.setText("00:00")
            self._total_label.setText("00:00")
            self._line_chip.setText("")
            self._layer_total = 0
            self._update_chips()

    def set_marks(self, marks: TimelineMarks) -> None:
        self._total_label.setText(format_duration(marks.total))

    def set_position(self, line: int, source: str, layer: int, layer_total: int, active: bool) -> None:
        """linha do G-code em execução e camada atual. active = processo ligado."""
        if len(source) > LINE_CHIP_MAX_CHARS:
            source = source[:LINE_CHIP_MAX_CHARS - 1] + "…"
        dot = ACCENT_TEXT if active else TEXT_MUTED
        self._line_chip.setText(f'<span style="color:{dot}">●</span>&nbsp; L{line}&nbsp;&nbsp;{escape(source)}')
        self._line_chip.setToolTip(tr("chip_process_on" if active else "chip_process_off"))
        self._layer_total = layer_total
        self._layer_chip.setText(tr("player_layer_chip").format(layer=layer, total=layer_total))
        self._update_chips()

    def set_chips_allowed(self, allowed: bool) -> None:
        """com o editor aberto a linha já aparece destacada lá; os chips seriam repetição."""
        self._chips_allowed = allowed
        self._update_chips()

    def _update_chips(self) -> None:
        """mensagem tem prioridade; sem ela, aparecem os chips de linha e camada."""
        free = self._chips_allowed and not self._message.text()
        self._line_chip.setVisible(free and bool(self._line_chip.text()))
        self._layer_chip.setVisible(free and self._layer_total > 1)

    def set_playing(self, playing: bool) -> None:
        self._play_button.setIcon(icon(PAUSE if playing else PLAY, ON_ACCENT))

    def set_progress(self, fraction: float, elapsed: float) -> None:
        with _signals_blocked(self._timeline):
            self._timeline.setValue(round(fraction * TIMELINE_STEPS))
        self._elapsed_label.setText(format_duration(elapsed))

    def set_speed(self, value: float) -> None:
        with _signals_blocked(self._speed_slider):
            self._speed_slider.setValue(round(value * SPEED_SLIDER_SCALE))
        self._speed_button.setText(f"{value:.1f}x  ▾")
        for preset, action in self._speed_actions:
            action.setChecked(math.isclose(preset, value))

    def set_status(self, text: str, timeout_ms: int = MESSAGE_TIMEOUT_MS) -> None:
        """mensagem à esquerda do transporte. timeout_ms=0 deixa a mensagem fixa."""
        self._message.setText(text)
        self._message.setToolTip(text)
        self._update_chips()
        self._message_timer.stop()
        if text and timeout_ms > 0:
            self._message_timer.start(timeout_ms)

    @staticmethod
    def _make_button(button_icon, tip: str, callback, size, name: str | None = None) -> QPushButton:
        button = _HoverGrowButton()
        button.setIcon(button_icon)
        button.setIconSize(QSize(round(size[0] * 0.5), round(size[1] * 0.5)))
        button.setToolTip(tip)
        button.setFixedSize(*size)
        if name:
            button.setObjectName(name)
        button.clicked.connect(lambda _checked=False: callback())
        return button