# Changelog — paint-crawl

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
