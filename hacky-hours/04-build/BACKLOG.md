# Backlog — paint-crawl

## MVP

- [x] Implement crawler: discover mediums from index page, crawl each medium
- [x] Implement parser: extract brand, name, hex, source URL from HTML
- [x] Implement normalizer: hex conversion, deduplication, missing field handling, whitespace trimming
- [x] Implement writer: produce wrapped JSON files in `data/`
- [x] Add HTML test fixtures and write unit tests (parser, normalizer, writer)
- [x] Write output validation tests and configure `pytest.ini`
- [x] Run first crawl, populate `data/`, set `tests/thresholds.json`
