from core.file_io import read_gcode_text


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