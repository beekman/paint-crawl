# Roadmap — paint-crawl

## MVP — "Run the crawler locally, get valid JSON output"

The crawler runs on the command line and produces correct, normalized JSON files for all mediums on art-paints.com. The mixing app can import the output. Unit tests and output validation pass.

| Feature | Notes |
|---------|-------|
| Project structure: `crawler.py`, `parser.py`, `normalizer.py`, `writer.py`, `requirements.txt` | |
| robots.txt check before crawling | Stop if disallowed, warn if unreachable |
| Crawler: discover mediums from index, crawl each medium | Dynamic discovery — no hardcoded list |
| Parser: extract brand, name, hex, source URL from HTML | |
| Normalizer: hex conversion, deduplication, missing field handling, whitespace trimming | See BUSINESS_LOGIC.md |
| Writer: one wrapped JSON file per medium to `data/` | See DATA_MODEL.md |
| `.gitignore` covering sensitive files | |
| Pinned dependencies in `requirements.txt` | Python 3.12, requests, beautifulsoup4 |
| HTML test fixtures + unit tests (parser, normalizer, writer) | |
| Output validation tests + `pytest.ini` | |
| Run first crawl, populate `data/`, set `tests/thresholds.json` | Thresholds = ~80% of initial count |

---

## V1 — "Stays up to date automatically, handles network hiccups"

The crawler runs on a schedule via GitHub Actions and commits fresh data to the repo weekly. Retry logic handles transient network errors gracefully.

| Feature | Notes |
|---------|-------|
| Retry logic: 429/503 wait-and-retry | 30s wait, retry once, then skip and log |
| GitHub Actions workflow: weekly schedule + manual dispatch | `.github/workflows/crawl.yml` |
| Integration tests | Network-required, marked, excluded from default CI |

---

## V2+

| Feature | Notes |
|---------|-------|
| Filtering and search capabilities | For mixing app to query dataset directly |
| Additional source sites beyond art-paints.com | Requires new parsers per site |
