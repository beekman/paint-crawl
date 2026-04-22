import json
import re
import pytest
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
THRESHOLDS_FILE = Path(__file__).parent / "thresholds.json"
HEX_RE = re.compile(r"^#[0-9a-f]{6}$")
REQUIRED_FIELDS = {"medium", "brand", "name", "hex_available", "source_url"}


def load_thresholds():
    if not THRESHOLDS_FILE.exists():
        return {}
    return json.loads(THRESHOLDS_FILE.read_text())


def get_data_files():
    if not DATA_DIR.exists():
        return []
    return list(DATA_DIR.glob("*.json"))


@pytest.mark.parametrize("data_file", get_data_files(), ids=lambda f: f.stem)
class TestOutputFiles:
    def test_envelope_fields(self, data_file):
        data = json.loads(data_file.read_text())
        assert "medium" in data
        assert "crawled_at" in data
        assert "paints" in data

    def test_paints_is_list(self, data_file):
        data = json.loads(data_file.read_text())
        assert isinstance(data["paints"], list)

    def test_entry_required_fields(self, data_file):
        data = json.loads(data_file.read_text())
        for entry in data["paints"]:
            missing = REQUIRED_FIELDS - entry.keys()
            assert not missing, f"Entry missing fields {missing}: {entry}"

    def test_hex_format(self, data_file):
        data = json.loads(data_file.read_text())
        for entry in data["paints"]:
            h = entry.get("hex")
            assert h is None or HEX_RE.match(h), f"Bad hex {h!r} in {entry}"

    def test_hex_available_consistent_with_hex(self, data_file):
        data = json.loads(data_file.read_text())
        for entry in data["paints"]:
            if entry["hex"] is None:
                assert entry["hex_available"] is False
            else:
                assert entry["hex_available"] is True

    def test_source_url_from_expected_domain(self, data_file):
        data = json.loads(data_file.read_text())
        for entry in data["paints"]:
            assert entry["source_url"].startswith("http://www.art-paints.com"), \
                f"Unexpected source_url: {entry['source_url']}"

    def test_minimum_paint_count(self, data_file):
        thresholds = load_thresholds()
        minimum = thresholds.get(data_file.stem)
        if minimum is None:
            pytest.skip(f"No threshold set for {data_file.stem}")
        data = json.loads(data_file.read_text())
        count = len(data["paints"])
        assert count >= minimum, \
            f"{data_file.stem}: {count} paints < threshold {minimum}"
