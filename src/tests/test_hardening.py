import json

import pytest

import config
from core.parser import ERROR, parse_gcode
from core.profile_store import load_profiles


def test_move_count_is_capped(monkeypatch):
    monkeypatch.setattr("core.parser.MAX_MOVES", 50)
    result = parse_gcode("G1 X50 Y50 F1000\n" + "G2 X50 Y50 I5 J0\n" * 10)
    assert len(result.moves) == 50
    assert [issue.severity for issue in result.issues] == [ERROR]


@pytest.fixture
def profiles_file(tmp_path, monkeypatch):
    path = tmp_path / "profiles.json"
    monkeypatch.setattr(config, "PROFILES_FILE", path)
    return path


def _write(path, **fields):
    profile = {"name": "teste", "limits": {"X": [0, 300], "Y": [0, 200], "Z": [-100, 100]}, **fields}
    path.write_text(json.dumps({"active": "teste", "profiles": [profile]}), encoding="utf-8")


def test_out_of_range_numbers_fall_back_to_defaults(profiles_file):
    _write(profiles_file, rapid_feed=0, arc_step_deg=1e-9, default_feed=float("nan"), min_feed="abc")
    profile = load_profiles()[0][0]
    assert profile.rapid_feed == config.RAPID_FEED
    assert profile.arc_step_deg == config.ARC_STEP_DEG
    assert profile.default_feed == config.DEFAULT_FEED
    assert profile.min_feed == config.MIN_FEED


def test_unknown_mode_and_dialect_fall_back(profiles_file):
    _write(profiles_file, mode="inexistente", dialect="outro")
    profile = load_profiles()[0][0]
    assert (profile.mode_key, profile.dialect_key) == (config.DEFAULT_MODE, config.DEFAULT_DIALECT)


def test_inverted_or_missing_limits_fall_back(profiles_file):
    _write(profiles_file, limits={"X": [300, 0], "Y": [0, 150]})
    limits = load_profiles()[0][0].limits
    assert limits == {"X": (0.0, 300.0), "Y": (0.0, 150.0), "Z": (-100.0, 100.0)}


def test_valid_profile_is_kept(profiles_file):
    _write(profiles_file, mode="deposicao", dialect="arco-m8-m9", rapid_feed=6000)
    profile = load_profiles()[0][0]
    assert (profile.mode_key, profile.dialect_key, profile.rapid_feed) == ("deposicao", "arco-m8-m9", 6000.0)