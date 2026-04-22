# Licensing — paint-crawl

## Project License

paint-crawl is a **private repository**. No license file is required or included. The code is not open source and is not distributed.

---

## Runtime Dependencies

| Package | License | Notes |
|---|---|---|
| `requests` | Apache 2.0 | Permissive — no restrictions on private use |
| `beautifulsoup4` | MIT | Permissive — no restrictions on private use |

No license conflicts. Both licenses are compatible with private, non-distributed use.

---

## Python Version

Target: **Python 3.12** (current stable). Pin in `requirements.txt` and GitHub Actions workflow.

---

## Crawled Data

paint-crawl fetches publicly listed paint data from art-paints.com. The crawled data (color names, hex values, brand names) is factual/descriptive information. It is stored in a private repository and used as internal tooling input — not redistributed publicly.

Before making the data or this tool public, review art-paints.com's terms of service.

---

## Adding Dependencies

Before adding any new dependency, check its license at [choosealicense.com](https://choosealicense.com) or via `pip show <package>`. Update this document with the new entry.
