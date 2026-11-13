import pytest

import config
from core.file_safety import UnsafeFileError, check_file_size, check_line_lengths


def test_small_file_is_accepted(tmp_path):
    path = tmp_path / "ok.nc"
    path.write_text("G1 X1", encoding="utf-8")
    check_file_size(path)


def test_large_file_is_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr("core.file_safety.MAX_FILE_SIZE_BYTES", 10)
    path = tmp_path / "big.nc"
    path.write_text("G1 X1 Y1 Z1 F100", encoding="utf-8")
    with pytest.raises(UnsafeFileError):
        check_file_size(path)


def test_long_line_is_rejected():
    with pytest.raises(UnsafeFileError, match=r"\b2\b"):
        check_line_lengths("G1 X1\n" + "X" * (config.MAX_LINE_LENGTH + 1))


def test_normal_lines_are_accepted():
    check_line_lengths("G1 X1\nG1 Y1")