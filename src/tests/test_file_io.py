import pytest

from core.file_io import read_gcode_text, write_text_atomic

def test_utf8_file(tmp_path):
    path = tmp_path / "a.nc"
    path.write_text("(Peça) G1 X1", encoding="utf-8")
    assert read_gcode_text(path) == ("(Peça) G1 X1", "utf-8")


def test_windows_1252_file_keeps_accents(tmp_path):
    path = tmp_path / "b.nc"
    path.write_bytes("(Peça) G1 X1".encode("cp1252"))
    text, encoding = read_gcode_text(path)
    assert text == "(Peça) G1 X1"
    path.write_text(text, encoding=encoding)
    assert path.read_bytes() == "(Peça) G1 X1".encode("cp1252")



def test_read_normalizes_windows_newlines(tmp_path):
    path = tmp_path / "crlf.nc"
    path.write_bytes(b"G1 X1\r\nG1 X2\r\n")
    assert read_gcode_text(path)[0] == "G1 X1\nG1 X2\n"


def test_atomic_write_replaces_content_and_leaves_no_temp(tmp_path):
    path = tmp_path / "a.nc"
    path.write_text("antigo", encoding="utf-8")
    write_text_atomic(path, "novo", "utf-8")
    assert path.read_text(encoding="utf-8") == "novo"
    assert [p.name for p in tmp_path.iterdir()] == ["a.nc"]


def test_atomic_write_keeps_original_when_encoding_fails(tmp_path):
    path = tmp_path / "b.nc"
    path.write_bytes("(Peça)".encode("cp1252"))
    with pytest.raises(UnicodeEncodeError):
        write_text_atomic(path, "(日本)", "cp1252")
    assert path.read_bytes() == "(Peça)".encode("cp1252")
    assert [p.name for p in tmp_path.iterdir()] == ["b.nc"]


def test_atomic_write_keeps_original_when_replace_fails(tmp_path, monkeypatch):
    path = tmp_path / "c.nc"
    path.write_text("antigo", encoding="utf-8")

    def broken_replace(source, target):
        raise OSError("disco cheio")

    monkeypatch.setattr("core.file_io.os.replace", broken_replace)
    with pytest.raises(OSError):
        write_text_atomic(path, "novo", "utf-8")
    assert path.read_text(encoding="utf-8") == "antigo"
    assert [p.name for p in tmp_path.iterdir()] == ["c.nc"]


def test_atomic_write_creates_new_file(tmp_path):
    path = tmp_path / "novo.nc"
    write_text_atomic(path, "G1 X1", "utf-8")
    assert path.read_text(encoding="utf-8") == "G1 X1"