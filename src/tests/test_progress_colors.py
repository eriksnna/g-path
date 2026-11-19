import numpy as np
import pytest

from ui.progress_colors import ProgressColors

DIM = np.array([0.2, 0.2, 0.2, 0.4])
BRIGHT = np.array([1.0, 0.5, 0.0, 1.0])


def _expected(is_cut, started, hidden=None):
    """o cálculo antigo, refeito do zero a cada quadro: serve de referência."""
    lit = np.arange(len(is_cut)) < started
    colors = np.where(lit[:, None], BRIGHT, DIM)
    if hidden is not None:
        colors[hidden, 3] = 0.0
    return np.repeat(colors[is_cut], 2, axis=0), np.repeat(colors[~is_cut], 2, axis=0)


def _make(is_cut, hidden=None):
    n = len(is_cut)
    return ProgressColors(is_cut, np.tile(DIM, (n, 1)), np.tile(BRIGHT, (n, 1)), hidden)


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_matches_full_recompute_going_forward_and_back(seed):
    rng = np.random.default_rng(seed)
    is_cut = rng.random(500) < 0.7
    hidden = rng.random(500) < 0.2
    colors = _make(is_cut, hidden)
    for started in [0, 3, 3, 120, 499, 500, 250, 0, 17, 500]:
        colors.update(started)
        cut, rapid = _expected(is_cut, started, hidden)
        assert np.array_equal(colors.cut, cut)
        assert np.array_equal(colors.rapid, rapid)


def test_reports_whether_something_changed():
    colors = _make(np.array([True, False, True]))
    assert colors.update(0) is False
    assert colors.update(2) is True
    assert colors.update(2) is False


def test_program_with_only_one_kind_of_move():
    colors = _make(np.ones(4, dtype=bool))
    colors.update(4)
    assert colors.rapid.shape == (0, 4)
    assert np.array_equal(colors.cut, np.tile(BRIGHT, (8, 1)))