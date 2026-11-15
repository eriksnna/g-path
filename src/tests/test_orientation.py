import pytest

from core.orientation import project_axes


def _close(found, expected):
    return all(abs(f - e) < 1e-9 for f, e in zip(found, expected))


def test_top_view_shows_x_right_and_y_up():
    x, y, z = project_axes(90.0, -90.0)
    assert _close(x, (1, 0, 0))
    assert _close(y, (0, 1, 0))
    assert _close(z, (0, 0, 1))  # Z aponta para a câmera


def test_front_view_shows_x_right_and_z_up():
    x, y, z = project_axes(0.0, -90.0)
    assert _close(x, (1, 0, 0))
    assert _close(z, (0, 1, 0))
    assert _close(y, (0, 0, -1))  # Y aponta para longe


def test_side_view_shows_y_right_and_z_up():
    x, y, z = project_axes(0.0, 0.0)
    assert _close(y, (1, 0, 0))
    assert _close(z, (0, 1, 0))
    assert _close(x, (0, 0, 1))


@pytest.mark.parametrize("elevation,azimuth", [(30, -60), (12, 200), (-45, 75)])
def test_axes_keep_unit_length(elevation, azimuth):
    for right, up, depth in project_axes(elevation, azimuth):
        assert abs(right * right + up * up + depth * depth - 1) < 1e-9