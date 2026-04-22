import pytest
import re

HEX_RE = re.compile(r"^#[0-9a-f]{6}$")


@pytest.mark.integration
def test_crawler_completes_without_errors():
    import requests
    from parser import parse_index

    session = requests.Session()
    session.headers["User-Agent"] = "paint-crawl/1.0"
    response = session.get("http://www.art-paints.com/Paints/Art-Paints.html")
    response.raise_for_status()
    mediums = parse_index(response.text)
    assert len(mediums) > 0


@pytest.mark.integration
def test_at_least_one_medium_discovered():
    import requests
    from parser import parse_index

    session = requests.Session()
    session.headers["User-Agent"] = "paint-crawl/1.0"
    html = session.get("http://www.art-paints.com/Paints/Art-Paints.html").text
    mediums = parse_index(html)
    assert len(mediums) >= 10


@pytest.mark.integration
def test_paint_entries_conform_to_schema():
    """Crawl one medium end-to-end and validate every entry."""
    import time
    import requests
    from parser import parse_index, is_color_page, parse_brand_links, parse_paints
    from normalizer import normalize_paint, deduplicate

    session = requests.Session()
    session.headers["User-Agent"] = "paint-crawl/1.0"

    html = session.get("http://www.art-paints.com/Paints/Art-Paints.html").text
    mediums = parse_index(html)
    slug, url = next(iter(mediums.items()))

    visited = set()

    def crawl(u):
        if u in visited:
            return []
        visited.add(u)
        time.sleep(2)
        h = session.get(u).text
        if is_color_page(h):
            return [dict(p, medium=slug) for p in parse_paints(h, u)]
        result = []
        for link in parse_brand_links(h, u):
            result.extend(crawl(link))
        return result

    raw = crawl(url)
    paints = [normalize_paint(p) for p in raw]
    paints = [p for p in paints if p is not None]
    paints = deduplicate(paints)

    assert len(paints) > 0
    required = {"medium", "brand", "name", "hex", "hex_available", "source_url"}
    for p in paints:
        assert required <= p.keys()
        assert p["hex"] is None or HEX_RE.match(p["hex"])
        assert p["hex_available"] == (p["hex"] is not None)
