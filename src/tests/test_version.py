import re
from pathlib import Path

import config


def test_version_matches_changelog():
    changelog = Path(__file__).resolve().parents[2] / "CHANGELOG.md"
    latest = re.search(r"^## \[([^\]]+)\]", changelog.read_text(encoding="utf-8"), re.M).group(1)
    assert config.APP_VERSION == latest