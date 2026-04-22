import time
import requests
from parser import parse_index, parse_medium
from normalizer import normalize_paint
from writer import write_medium

INDEX_URL = "http://www.art-paints.com/Paints/Art-Paints.html"
DELAY = 2


def fetch(url, session):
    response = session.get(url)
    response.raise_for_status()
    return response.text


def crawl():
    session = requests.Session()
    session.headers["User-Agent"] = "paint-crawl/1.0"

    index_html = fetch(INDEX_URL, session)
    mediums = parse_index(index_html)

    for medium, medium_url in mediums.items():
        time.sleep(DELAY)
        medium_html = fetch(medium_url, session)
        raw_paints = parse_medium(medium_html, medium_url)
        paints = [normalize_paint(p) for p in raw_paints]
        paints = [p for p in paints if p is not None]
        write_medium(medium, paints)
        print(f"{medium}: {len(paints)} paints")


if __name__ == "__main__":
    crawl()
