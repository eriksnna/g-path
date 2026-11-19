import pytest

from core.document import Document
from core.file_safety import UnsafeFileError


def _file(tmp_path, name="a.nc", data="G1 X1\n", encoding="utf-8"):
    path = tmp_path / name
    path.write_bytes(data.encode(encoding))
    return path


def test_open_sets_everything(tmp_path):
    path = _file(tmp_path, data="(Peça)\n", encoding="cp1252")
    doc = Document()
    doc.open(path)
    assert (doc.path, doc.text, doc.saved_text, doc.encoding) == (path, "(Peça)\n", "(Peça)\n", "cp1252")
    assert not doc.has_unsaved_changes()


def test_failed_open_keeps_the_previous_program(tmp_path):
    doc = Document()
    doc.open(_file(tmp_path))
    with pytest.raises(OSError):
        doc.open(tmp_path / "nao_existe.nc")
    assert doc.text == "G1 X1\n" and doc.path.name == "a.nc"


def test_unsafe_file_is_rejected(tmp_path):
    doc = Document()
    with pytest.raises(UnsafeFileError):
        doc.open(_file(tmp_path, data="G1 X" + "1" * 100_000))
    assert doc.text is None


def test_applied_edit_is_unsaved_until_saved(tmp_path):
    doc = Document()
    doc.open(_file(tmp_path))
    doc.apply("G1 X2\n")
    assert doc.has_unsaved_changes()
    doc.save("G1 X2\n")
    assert not doc.has_unsaved_changes()
    assert (tmp_path / "a.nc").read_text(encoding="utf-8") == "G1 X2\n"


def test_editor_modification_counts_as_unsaved(tmp_path):
    doc = Document()
    doc.open(_file(tmp_path))
    assert doc.has_unsaved_changes(editor_modified=True)


def test_nothing_open_has_nothing_unsaved():
    assert not Document().has_unsaved_changes(editor_modified=True)


def test_save_as_moves_the_document(tmp_path):
    doc = Document()
    doc.new_blank()
    target = tmp_path / "novo.nc"
    doc.save("G0 X0\n", target)
    assert doc.path == target and doc.saved_text == "G0 X0\n"


def test_save_without_path_is_refused():
    doc = Document()
    doc.new_blank()
    with pytest.raises(ValueError):
        doc.save("G0 X0\n")


def test_save_falls_back_to_utf8_when_encoding_cannot_hold_the_text(tmp_path):
    path = _file(tmp_path, data="(Peça)\n", encoding="cp1252")
    doc = Document()
    doc.open(path)
    doc.save("(日本)\n")
    assert doc.encoding == "utf-8"
    assert path.read_text(encoding="utf-8") == "(日本)\n"


def test_failed_save_changes_nothing(tmp_path, monkeypatch):
    doc = Document()
    doc.open(_file(tmp_path))
    doc.apply("G1 X9\n")

    def broken(*_args):
        raise OSError("disco cheio")

    monkeypatch.setattr("core.document.write_text_atomic", broken)
    with pytest.raises(OSError):
        doc.save("G1 X9\n")
    assert doc.saved_text == "G1 X1\n" and doc.has_unsaved_changes()


def test_changed_on_disk_ignores_our_own_save(tmp_path):
    doc = Document()
    doc.open(_file(tmp_path))
    doc.save("G1 X5\n")
    assert doc.changed_on_disk() is None


def test_changed_on_disk_reports_another_programs_edit(tmp_path):
    path = _file(tmp_path)
    doc = Document()
    doc.open(path)
    path.write_bytes(b"G1 X7\r\n")
    assert doc.changed_on_disk() == ("G1 X7\n", "utf-8")
    doc.take_disk_version("G1 X7\n", "utf-8")
    assert not doc.has_unsaved_changes()


def test_changed_on_disk_without_file(tmp_path):
    path = _file(tmp_path)
    doc = Document()
    doc.open(path)
    path.unlink()
    assert doc.changed_on_disk() is None


def test_close_forgets_everything(tmp_path):
    doc = Document()
    doc.open(_file(tmp_path))
    doc.close()
    assert (doc.path, doc.text, doc.saved_text) == (None, None, None)