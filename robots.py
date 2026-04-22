from urllib.robotparser import RobotFileParser
from urllib.error import URLError


ROBOTS_URL = "http://www.art-paints.com/robots.txt"
USER_AGENT = "paint-crawl"


def check_robots(index_url):
    rp = RobotFileParser()
    rp.set_url(ROBOTS_URL)
    try:
        rp.read()
    except (URLError, OSError):
        print("WARNING: could not fetch robots.txt — proceeding anyway")
        return

    if not rp.can_fetch(USER_AGENT, index_url):
        raise PermissionError(
            f"robots.txt disallows crawling {index_url} — stopping"
        )
