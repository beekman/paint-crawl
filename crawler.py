import time
import requests
from parser import parse_index, is_color_page, parse_brand_links, parse_paints
from normalizer import normalize_paint, deduplicate
from robots import check_robots
from writer import write_medium

INDEX_URL = "http://www.art-paints.com/Paints/Art-Paints.html"
DELAY = 1


def fetch(url, session):
    for attempt in range(2):
        response = session.get(url)
        if response.status_code in (429, 503):
            if attempt == 0:
                print(f"WARNING: {response.status_code} on {url} — retrying in 30s")
                time.sleep(30)
                continue
            print(f"SKIP (HTTP {response.status_code} after retry): {url}")
            return None
        if not response.ok:
            print(f"SKIP (HTTP {response.status_code}): {url}")
            return None
        return response.text
    return None


def crawl_url(url, medium_slug, session, visited):
    """Recursively crawl a URL, returning list of raw paint dicts."""
    if url in visited:
        return []
    visited.add(url)
    time.sleep(DELAY)
    html = fetch(url, session)
    if html is None:
        return []
    if is_color_page(html):
        return [dict(p, medium=medium_slug) for p in parse_paints(html, url)]
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
        paints = deduplicate(paints)
        write_medium(medium_slug, paints)
        print(f"{medium_slug}: {len(paints)} paints")


if __name__ == "__main__":
    crawl()
