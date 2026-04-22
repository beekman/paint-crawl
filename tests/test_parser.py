import pytest
from pathlib import Path
from parser import parse_index, is_color_page, parse_brand_links, parse_paints

FIXTURES = Path(__file__).parent / "fixtures"
INDEX_URL = "http://www.art-paints.com/Paints/Art-Paints.html"
MEDIUM_URL = "http://www.art-paints.com/Paints/Watercolor/Watercolor-Paint.html"
PAINT_URL = "http://www.art-paints.com/Paints/Watercolor/American-Journey/Iridescent/American-Journey-Iridescent.html"


@pytest.fixture
def index_html():
    return (FIXTURES / "sample_index.html").read_text(encoding="utf-8")


@pytest.fixture
def medium_html():
    return (FIXTURES / "sample_medium.html").read_text(encoding="utf-8")


@pytest.fixture
def paint_html():
    return (FIXTURES / "sample_paint.html").read_text(encoding="utf-8")


class TestParseIndex:
    def test_discovers_mediums(self, index_html):
        mediums = parse_index(index_html)
        assert len(mediums) == 21

    def test_watercolor_present(self, index_html):
        mediums = parse_index(index_html)
        assert "watercolor-paint" in mediums

    def test_watercolor_url(self, index_html):
        mediums = parse_index(index_html)
        assert mediums["watercolor-paint"] == MEDIUM_URL

    def test_excludes_index_page(self, index_html):
        mediums = parse_index(index_html)
        assert INDEX_URL not in mediums.values()

    def test_no_duplicate_urls(self, index_html):
        mediums = parse_index(index_html)
        assert len(set(mediums.values())) == len(mediums)


class TestIsColorPage:
    def test_medium_is_not_color_page(self, medium_html):
        assert is_color_page(medium_html) is False

    def test_paint_page_is_color_page(self, paint_html):
        assert is_color_page(paint_html) is True


class TestParseBrandLinks:
    def test_returns_links(self, medium_html):
        links = parse_brand_links(medium_html, MEDIUM_URL)
        assert len(links) > 0

    def test_links_within_medium_subtree(self, medium_html):
        links = parse_brand_links(medium_html, MEDIUM_URL)
        base = "http://www.art-paints.com/Paints/Watercolor/"
        assert all(l.startswith(base) for l in links)

    def test_no_self_links(self, medium_html):
        links = parse_brand_links(medium_html, MEDIUM_URL)
        assert MEDIUM_URL not in links

    def test_no_duplicates(self, medium_html):
        links = parse_brand_links(medium_html, MEDIUM_URL)
        assert len(links) == len(set(links))


class TestParsePaints:
    def test_returns_paints(self, paint_html):
        paints = parse_paints(paint_html, PAINT_URL)
        assert len(paints) == 15

    def test_brand_extracted(self, paint_html):
        paints = parse_paints(paint_html, PAINT_URL)
        assert paints[0]["brand"] == "American Journey"

    def test_name_extracted(self, paint_html):
        paints = parse_paints(paint_html, PAINT_URL)
        assert paints[0]["name"] == "Hot Tamale"

    def test_hex_extracted(self, paint_html):
        paints = parse_paints(paint_html, PAINT_URL)
        assert paints[0]["hex"] == "#EC5C5F"

    def test_source_url_set(self, paint_html):
        paints = parse_paints(paint_html, PAINT_URL)
        assert paints[0]["source_url"] == PAINT_URL

    def test_paint_suffix_stripped_from_name(self, paint_html):
        paints = parse_paints(paint_html, PAINT_URL)
        assert not any(p["name"].endswith(" Paint") for p in paints)
