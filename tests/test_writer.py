import json
import re
import pytest
from pathlib import Path
from datetime import datetime, timezone
from writer import write_medium


@pytest.fixture
def tmp_output(tmp_path):
    return tmp_path


SAMPLE_PAINTS = [
    {"medium": "oils", "brand": "Winsor", "name": "Cadmium Red",
     "hex": "#e32636", "hex_available": True, "source_url": "http://x.com"},
]


class TestWriteMedium:
    def test_file_created(self, tmp_output):
        write_medium("oils", SAMPLE_PAINTS, output_dir=str(tmp_output))
        assert (tmp_output / "oils.json").exists()

    def test_envelope_fields_present(self, tmp_output):
        write_medium("oils", SAMPLE_PAINTS, output_dir=str(tmp_output))
        data = json.loads((tmp_output / "oils.json").read_text())
        assert "medium" in data
        assert "crawled_at" in data
        assert "paints" in data

    def test_medium_field_correct(self, tmp_output):
        write_medium("oils", SAMPLE_PAINTS, output_dir=str(tmp_output))
        data = json.loads((tmp_output / "oils.json").read_text())
        assert data["medium"] == "oils"

    def test_paints_written(self, tmp_output):
        write_medium("oils", SAMPLE_PAINTS, output_dir=str(tmp_output))
        data = json.loads((tmp_output / "oils.json").read_text())
        assert len(data["paints"]) == 1
        assert data["paints"][0]["name"] == "Cadmium Red"

    def test_crawled_at_is_iso8601(self, tmp_output):
        write_medium("oils", SAMPLE_PAINTS, output_dir=str(tmp_output))
        data = json.loads((tmp_output / "oils.json").read_text())
        ts = data["crawled_at"]
        # Should parse without error and be timezone-aware
        dt = datetime.fromisoformat(ts)
        assert dt.tzinfo is not None

    def test_creates_output_dir_if_missing(self, tmp_output):
        nested = tmp_output / "nested" / "dir"
        write_medium("oils", SAMPLE_PAINTS, output_dir=str(nested))
        assert (nested / "oils.json").exists()

    def test_empty_paints_list(self, tmp_output):
        write_medium("oils", [], output_dir=str(tmp_output))
        data = json.loads((tmp_output / "oils.json").read_text())
        assert data["paints"] == []
