# Changelog — paint-crawl

## v0.3.0 — RGB field (2026-04-25)

### What's included
- Each paint entry now includes an `rgb` field (e.g. `"236, 92, 95"`), computed
  directly from the normalized hex value — no additional HTTP requests required
- Crawl delay reduced from 2s to 1s per page
- 220 tests passing

### Data
- 21 mediums, 55,790 paints (up from 53,789)
- Crawled from art-paints.com on 2026-04-25

---

## v0.2.0 — V1 (2026-04-22)

### What's included
- GitHub Actions workflow: weekly automated crawl every Monday at 04:00 UTC,
  with manual dispatch available
- Commits updated data/ files back to main automatically; no-ops cleanly
  if nothing changed
- Retry logic for 429/503 responses: 30s wait, one retry, then skip and log
  (implemented during MVP build)

---

## v0.1.0 — MVP (2026-04-22)

First release of paint-crawl.

### What's included
- Crawler that recursively discovers all mediums and brands on art-paints.com
- Parser that extracts brand, name, and hex value from each paint page
- Normalizer that converts hex values to lowercase #rrggbb, handles duplicates,
  and skips entries missing brand or name
- Writer that produces one wrapped JSON file per medium in data/
- robots.txt check before crawling begins
- 197 tests passing: unit tests (parser, normalizer, writer), output validation
  against all 21 medium files with minimum count thresholds

### Data
- 21 mediums, 53,789 paints
- Crawled from art-paints.com on 2026-04-22
