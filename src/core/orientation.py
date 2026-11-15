"""projeção dos eixos do mundo na tela, a partir dos ângulos da câmera orbital."""
from __future__ import annotations

import math


def project_axes(elevation: float, azimuth: float) -> list[tuple[float, float, float]]:
    """para X, Y e Z: (direita, cima, profundidade) na tela, em graus de câmera.
    profundidade > 0 significa que o eixo aponta para quem olha."""
    e, a = math.radians(elevation), math.radians(azimuth)
    return [
        (-math.sin(a), -math.cos(a) * math.sin(e), math.cos(e) * math.cos(a)),
        (math.cos(a), -math.sin(a) * math.sin(e), math.cos(e) * math.sin(a)),
        (0.0, math.cos(e), math.sin(e)),
    ]