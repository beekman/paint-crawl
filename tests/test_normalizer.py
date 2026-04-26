import pytest
from normalizer import normalize_hex, normalize_paint, deduplicate


class TestNormalizeHex:
    def test_6digit_uppercase_lowercased(self):
        assert normalize_hex("#E32636") == "#e32636"

    def test_6digit_no_hash(self):
        assert normalize_hex("E32636") == "#e32636"

    def test_3digit_expanded(self):
        assert normalize_hex("#e36") == "#ee3366"

    def test_3digit_no_hash(self):
        assert normalize_hex("abc") == "#aabbcc"

    def test_rgb_converted(self):
        assert normalize_hex("rgb(227, 38, 54)") == "#e32636"

    def test_rgb_with_spaces(self):
        assert normalize_hex("rgb( 0, 0, 255 )") == "#0000ff"

    def test_hsl_converted(self):
        result = normalize_hex("hsl(0, 100%, 50%)")
        assert result == "#ff0000"

    def test_named_color_crimson(self):
        assert normalize_hex("crimson") == "#dc143c"

    def test_named_color_case_insensitive(self):
        assert normalize_hex("Crimson") == "#dc143c"

    def test_unrecognizable_returns_none(self):
        assert normalize_hex("notacolor") is None

    def test_none_returns_none(self):
        assert normalize_hex(None) is None

    def test_empty_string_returns_none(self):
        assert normalize_hex("") is None

    def test_result_always_valid_hex_format(self):
        import re
        valid = re.compile(r"^#[0-9a-f]{6}$")
        for v in ["#FF0000", "abc", "rgb(1,2,3)", "red"]:
            result = normalize_hex(v)
            assert result is None or valid.match(result)


class TestNormalizePaint:
    def _paint(self, **kwargs):
        base = {"medium": "oils", "brand": "Winsor", "name": "Cadmium Red",
                "hex": "#E32636", "source_url": "http://x.com"}
        base.update(kwargs)
        return base

    def test_returns_normalized_dict(self):
        result = normalize_paint(self._paint())
        assert result is not None
        assert result["brand"] == "Winsor"
        assert result["name"] == "Cadmium Red"
        assert result["hex"] == "#e32636"
        assert result["hex_available"] is True

    def test_whitespace_trimmed(self):
        result = normalize_paint(self._paint(brand=" Winsor ", name=" Cadmium Red "))
        assert result["brand"] == "Winsor"
        assert result["name"] == "Cadmium Red"

    def test_missing_brand_skipped(self):
        assert normalize_paint(self._paint(brand="")) is None

    def test_missing_name_skipped(self):
        assert normalize_paint(self._paint(name="")) is None

    def test_missing_hex_sets_null_and_unavailable(self):
        result = normalize_paint(self._paint(hex=None))
        assert result["hex"] is None
        assert result["hex_available"] is False

    def test_unrecognizable_hex_sets_null_and_unavailable(self):
        result = normalize_paint(self._paint(hex="notacolor"))
        assert result["hex"] is None
        assert result["hex_available"] is False

    def test_medium_preserved(self):
        result = normalize_paint(self._paint(medium="watercolor-paint"))
        assert result["medium"] == "watercolor-paint"

    def test_source_url_preserved(self):
        result = normalize_paint(self._paint(source_url="http://example.com"))
        assert result["source_url"] == "http://example.com"

    def test_rgb_computed_from_hex(self):
        result = normalize_paint(self._paint(hex="#EC5C5F"))
        assert result["rgb"] == "236, 92, 95"

    def test_rgb_none_when_hex_unavailable(self):
        result = normalize_paint(self._paint(hex=None))
        assert result["rgb"] is None


class TestDeduplicate:
    def _paint(self, name, hex_val):
        return {"medium": "oils", "brand": "Winsor", "name": name,
                "hex": hex_val, "hex_available": hex_val is not None,
                "source_url": "http://x.com"}

    def test_unique_paints_kept(self):
        paints = [self._paint("Red", "#ff0000"), self._paint("Blue", "#0000ff")]
        assert len(deduplicate(paints)) == 2

    def test_duplicate_removed(self):
        paints = [self._paint("Red", "#ff0000"), self._paint("Red", "#ee0000")]
        result = deduplicate(paints)
        assert len(result) == 1

    def test_keeps_first_with_valid_hex(self):
        paints = [self._paint("Red", None), self._paint("Red", "#ff0000")]
        result = deduplicate(paints)
        assert result[0]["hex"] == "#ff0000"

    def test_keeps_first_when_no_hex_available(self):
        paints = [self._paint("Red", None), self._paint("Red", None)]
        result = deduplicate(paints)
        assert len(result) == 1

    def test_dedup_case_insensitive(self):
        p1 = self._paint("Cadmium Red", "#e32636")
        p2 = dict(p1, name="cadmium red")
        result = deduplicate([p1, p2])
        assert len(result) == 1
