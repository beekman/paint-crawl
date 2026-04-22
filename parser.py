from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

BASE_URL = "http://www.art-paints.com"
INDEX_URL = "http://www.art-paints.com/Paints/Art-Paints.html"


def parse_index(html):
    """Returns {medium_slug: url} mapping, deduplicating by URL."""
    soup = BeautifulSoup(html, "html.parser")
    seen_urls = {}
    for a in soup.select("a[href]"):
        href = a.get("href", "")
        if not (href and "/Paints/" in href and href.endswith(".html")):
            continue
        url = urljoin(BASE_URL, href)
        if url == INDEX_URL or url in seen_urls:
            continue
        slug = urlparse(url).path.rstrip("/").split("/")[-1].replace(".html", "").lower()
        seen_urls[url] = slug
    return {slug: url for url, slug in seen_urls.items()}


def is_color_page(html):
    return "corners.gif" in html


def parse_brand_links(html, page_url):
    """Returns list of absolute URLs to sub-pages within the same medium subtree."""
    parsed = urlparse(page_url)
    base_dir = parsed.scheme + "://" + parsed.netloc + "/".join(parsed.path.split("/")[:-1]) + "/"
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.select("a[href]"):
        href = a.get("href", "")
        if not (href and href.endswith(".html")):
            continue
        url = urljoin(page_url, href)
        if url != page_url and url.startswith(base_dir):
            links.append(url)
    return list(dict.fromkeys(links))


def _brand_from_breadcrumb(soup):
    """Extracts brand name from breadcrumb (index 3: Home, Paints, Medium, Brand)."""
    crumbs = soup.find_all("font", style=lambda s: s and "font-size:12px" in s)
    if len(crumbs) >= 4:
        return crumbs[3].get_text(strip=True)
    if crumbs:
        return crumbs[-1].get_text(strip=True)
    return None


def parse_paints(html, page_url):
    """Returns list of raw paint dicts from a color listing page."""
    soup = BeautifulSoup(html, "html.parser")
    brand = _brand_from_breadcrumb(soup)
    paints = []
    for img in soup.find_all("img", src=lambda s: s and "corners.gif" in s):
        alt = img.get("alt", "")
        name = alt.replace(" Paint", "").strip()
        td = img.find_parent("td")
        hex_val = None
        if td:
            tr = td.find_parent("tr")
            if tr:
                swatch = tr.find("td", bgcolor=True)
                if swatch:
                    hex_val = swatch["bgcolor"].strip()
        if name:
            paints.append({
                "brand": brand,
                "name": name,
                "hex": hex_val,
                "source_url": page_url,
            })
    return paints
