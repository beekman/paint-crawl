import time
import requests
from parser import parse_index, is_color_page, parse_brand_links, parse_paints
from normalizer import normalize_paint
from robots import check_robots
from writer import write_medium

INDEX_URL = "http://www.art-paints.com/Paints/Art-Paints.html"
DELAY = 2


def fetch(url, session):
    response = session.get(url)
    response.raise_for_status()
    return response.text


def crawl_url(url, medium_slug, session, visited):
    """Recursively crawl a URL, returning list of raw paint dicts."""
    if url in visited:
        return []
    visited.add(url)
    time.sleep(DELAY)
    html = fetch(url, session)
    if is_color_page(html):
        return parse_paints(html, url)
    paints = []
    for link in parse_brand_links(html, url):
        paints.extend(crawl_url(link, medium_slug, session, visited))
    return paints


def crawl():
    check_robots(INDEX_URL)

    session = requests.Session()
    session.headers["User-Agent"] = "paint-crawl/1.0"

    index_html = fetch(INDEX_URL, session)
    mediums = parse_index(index_html)

    for medium_slug, medium_url in mediums.items():
        visited = set()
        raw_paints = crawl_url(medium_url, medium_slug, session, visited)
        paints = [normalize_paint(p) for p in raw_paints]
        paints = [p for p in paints if p is not None]
        write_medium(medium_slug, paints)
        print(f"{medium_slug}: {len(paints)} paints")


if __name__ == "__main__":
    crawl()
