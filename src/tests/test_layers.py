import numpy as np

from core.layers import RAPID_LAYER, depth_levels, filter_layers, layer_indices
from core.parser import Move
from core.toolpath import Toolpath


def make_path():
    # cortes em z=0 (início) e z=-5; um rápido de volta ao topo
    return Toolpath([
        Move((0, 0, 0), (10, 0, 0), is_cut=True, feed=600.0),
        Move((10, 0, 0), (10, 0, -5), is_cut=True, feed=600.0),
        Move((10, 0, -5), (0, 0, -5), is_cut=True, feed=600.0),
        Move((0, 0, -5), (0, 0, 0), is_cut=False, feed=0.0),
    ])


def test_depth_levels_are_sorted_and_unique():
    levels = depth_levels(make_path())
    assert levels.tolist() == [-5.0, 0.0]


def test_layer_indices_map_each_move_and_mark_rapids():
    path = make_path()
    indices = layer_indices(path, depth_levels(path))
    assert indices.tolist() == [1, 0, 0, RAPID_LAYER]


def test_no_cuts_means_no_levels():
    path = Toolpath([Move((0, 0, 0), (5, 0, 0), is_cut=False, feed=0.0)])
    assert depth_levels(path).size == 0
    assert np.all(layer_indices(path, depth_levels(path)) == RAPID_LAYER)

def test_filter_layers_include_travel_ending_on_a_level():
    # depósito por pontos: o trabalho são esperas; o que se vê são os deslocamentos
    path = Toolpath([
        Move((0, 0, 0), (0, 0, 0), is_cut=True, feed=0.0),       # ponto em z=0
        Move((0, 0, 0), (10, 0, 0), is_cut=False, feed=600.0),   # deslocamento na camada z=0
        Move((10, 0, 0), (10, 0, 5), is_cut=False, feed=600.0),  # sobe para a camada z=5
        Move((10, 0, 5), (10, 0, 5), is_cut=True, feed=0.0),     # ponto em z=5
        Move((10, 0, 5), (10, 0, 30), is_cut=False, feed=600.0), # recuo acima de todas as camadas
    ])
    layers = filter_layers(path, depth_levels(path))
    assert layers.tolist() == [0, 0, 1, 1, RAPID_LAYER]


def test_filter_layers_without_levels():
    path = Toolpath([Move((0, 0, 0), (5, 0, 0), is_cut=False, feed=0.0)])
    assert filter_layers(path, depth_levels(path)).tolist() == [RAPID_LAYER]