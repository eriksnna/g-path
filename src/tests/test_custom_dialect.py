import pytest

import config
from core.dialect import (
    CUSTOM_DIALECT, MILLISECONDS, SECONDS, DialectError, format_m_codes, get_dialect,
    make_custom_dialect, parse_m_codes, suggest_dialect,
)
from core.machine_profile import MachineProfile
from core.parser import parse_gcode
from core.profile_store import load_profiles, save_profiles


@pytest.mark.parametrize("text, expected", [
    ("M10", {10}),
    ("M10, M12", {10, 12}),
    ("10 12", {10, 12}),
    ("m10/m12", {10, 12}),
    ("M08;M8", {8}),
    ("", set()),
])
def test_parse_m_codes(text, expected):
    assert parse_m_codes(text) == expected


@pytest.mark.parametrize("text", ["M", "G1", "M10a", "dez"])
def test_parse_m_codes_rejects_garbage(text):
    with pytest.raises(DialectError):
        parse_m_codes(text)


def test_format_m_codes_is_sorted():
    assert format_m_codes({12, 10}) == "M10, M12"


def test_make_custom_dialect():
    dialect = make_custom_dialect({10}, {11}, MILLISECONDS)
    assert dialect.process_on == {10} and dialect.process_off == {11}
    assert dialect.dwell_unit == MILLISECONDS


@pytest.mark.parametrize("on, off, unit", [
    (set(), {11}, SECONDS),          # sem código de ligar
    ({10}, set(), SECONDS),          # sem código de desligar
    ({10}, {10, 11}, SECONDS),       # M10 nos dois
    ({30}, {11}, SECONDS),           # M30 é fim de programa
    ({10}, {99}, SECONDS),           # M99 é retorno de sub-rotina
    ({1000}, {11}, SECONDS),         # fora da faixa
    (set(range(3, 13)), {20}, SECONDS),  # códigos demais
    ({10}, {11}, 60.0),              # unidade inventada
])
def test_invalid_custom_dialects_are_refused(on, off, unit):
    with pytest.raises(DialectError):
        make_custom_dialect(on, off, unit)


def test_profile_uses_custom_dialect_only_when_selected():
    profile = MachineProfile("Teste")
    profile.custom_dialect = make_custom_dialect({10}, {11}, SECONDS)
    assert profile.dialect is get_dialect(config.DEFAULT_DIALECT)
    profile.dialect_key = CUSTOM_DIALECT
    assert profile.dialect.process_on == {10}


def test_parser_follows_custom_codes():
    dialect = make_custom_dialect({10}, {11}, SECONDS)
    moves = parse_gcode("M10\nG1 X10 F100\nM11\nG1 X20", dialect=dialect).moves
    assert [m.active for m in moves] == [True, False]


def test_custom_milliseconds_apply_to_p():
    dialect = make_custom_dialect({10}, {11}, MILLISECONDS)
    assert parse_gcode("G4 P1500", dialect=dialect).moves[0].dwell == pytest.approx(1.5)


def test_suggestion_respects_custom_codes():
    dialect = make_custom_dialect({8}, {9}, SECONDS)
    assert suggest_dialect("M8\nG1 X10 F100\nM9", dialect) is None


def test_custom_dialect_survives_save_and_load(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "PROFILES_FILE", tmp_path / "profiles.json")
    profile = MachineProfile("Célula WAAM", dialect_key=CUSTOM_DIALECT,
                             custom_dialect=make_custom_dialect({10, 12}, {11}, MILLISECONDS))
    save_profiles([profile], profile.name)
    loaded = load_profiles()[0][0]
    assert loaded.dialect_key == CUSTOM_DIALECT
    assert loaded.dialect.process_on == {10, 12}
    assert loaded.dialect.dwell_unit == MILLISECONDS


def test_broken_custom_dialect_falls_back_to_default(tmp_path, monkeypatch):
    path = tmp_path / "profiles.json"
    path.write_text('{"active": "A", "profiles": [{"name": "A", "dialect": "personalizado",'
                    ' "custom_dialect": {"on": [30], "off": "x", "dwell_unit": 7}}]}', encoding="utf-8")
    monkeypatch.setattr(config, "PROFILES_FILE", path)
    loaded = load_profiles()[0][0]
    assert loaded.dialect_key == CUSTOM_DIALECT
    assert loaded.dialect.process_on == get_dialect("generico").process_on


def test_old_profiles_without_custom_dialect_still_load(tmp_path, monkeypatch):
    path = tmp_path / "profiles.json"
    path.write_text('{"active": "A", "profiles": [{"name": "A", "dialect": "fanuc"}]}', encoding="utf-8")
    monkeypatch.setattr(config, "PROFILES_FILE", path)
    loaded = load_profiles()[0][0]
    assert loaded.dialect is get_dialect("fanuc")