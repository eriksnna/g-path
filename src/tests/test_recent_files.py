from config import MAX_RECENT_FILES
from core.recent_files import LAST_KEY, RECENT_KEY, RecentFiles


class FakeSettings:
    """o mínimo do QSettings que RecentFiles usa."""

    def __init__(self, values=None):
        self.values = dict(values or {})

    def value(self, key, default=None):
        return self.values.get(key, default)

    def setValue(self, key, value):
        self.values[key] = value

    def remove(self, key):
        self.values.pop(key, None)


def _files(tmp_path, *names):
    paths = []
    for name in names:
        path = tmp_path / name
        path.write_text("G0 X0", encoding="utf-8")
        paths.append(path)
    return paths


def test_opened_goes_to_the_top_without_duplicates(tmp_path):
    a, b = _files(tmp_path, "a.nc", "b.nc")
    recent = RecentFiles(FakeSettings())
    recent.opened(a)
    recent.opened(b)
    recent.opened(a)
    assert recent.existing() == [str(a), str(b)]
    assert recent.last_file() == a


def test_list_is_capped(tmp_path):
    paths = _files(tmp_path, *[f"{i}.nc" for i in range(MAX_RECENT_FILES + 3)])
    recent = RecentFiles(FakeSettings())
    for path in paths:
        recent.opened(path)
    assert len(recent.existing()) == MAX_RECENT_FILES


def test_missing_files_are_hidden(tmp_path):
    a, b = _files(tmp_path, "a.nc", "b.nc")
    recent = RecentFiles(FakeSettings())
    recent.opened(a)
    recent.opened(b)
    b.unlink()
    assert recent.existing() == [str(a)]
    assert recent.last_file() is None


def test_single_saved_item_comes_back_as_string(tmp_path):
    (a,) = _files(tmp_path, "a.nc")
    recent = RecentFiles(FakeSettings({RECENT_KEY: str(a)}))
    assert recent.existing() == [str(a)]


def test_forget_last_keeps_the_list(tmp_path):
    (a,) = _files(tmp_path, "a.nc")
    settings = FakeSettings()
    recent = RecentFiles(settings)
    recent.opened(a)
    recent.forget_last()
    assert LAST_KEY not in settings.values
    assert recent.existing() == [str(a)]