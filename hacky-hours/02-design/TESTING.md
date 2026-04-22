# Testing — paint-crawl

## Test Framework

**pytest** — run with `pytest tests/`

---

## Test Structure

```
tests/
  fixtures/
    sample_index.html       ← saved copy of the art-paints.com index page
    sample_medium.html      ← saved copy of a medium page (e.g., oils)
    sample_paint.html       ← saved copy of an individual paint page
  test_parser.py            ← unit tests for parser.py
  test_normalizer.py        ← unit tests for normalizer.py
  test_writer.py            ← unit tests for writer.py
  test_integration.py       ← live crawl tests (network required)
  test_output.py            ← validates generated JSON files in data/
```

---

## Unit Tests

### Parser (`test_parser.py`)
Feed saved HTML fixtures into the parser and assert correct output. No network required.

- Extracts correct brand, name, hex, and source URL from a known paint page
- Returns `hex: null` and `hex_available: false` when no color value is present
- Correctly discovers medium links from the index page
- Correctly discovers paint links from a medium page

### Normalizer (`test_normalizer.py`)
Test each conversion rule in isolation.

- 6-digit hex is lowercased
- 3-digit hex is expanded and lowercased
- RGB value is converted to lowercase hex
- HSL value is converted to lowercase hex
- Named CSS color is converted to lowercase hex
- Unrecognizable value produces `hex: null`, `hex_available: false`
- Duplicate resolution keeps the first entry with a valid hex value
- Whitespace is trimmed from brand and name fields
- Entries missing brand or name are skipped

### Writer (`test_writer.py`)
- Output file contains correct envelope fields (`medium`, `crawled_at`, `paints`)
- `crawled_at` is a valid ISO 8601 timestamp
- File is written to the correct path under `data/`

---

## Integration Tests (`test_integration.py`)

Requires network access. Not run in CI by default — run manually before a release.

- Crawler completes without HTTP errors
- At least one medium is discovered
- Each discovered medium produces a non-empty `paints` array
- All entries in the output conform to the paint entry schema

Run with: `pytest tests/test_integration.py -m integration`

Mark these tests with `@pytest.mark.integration` and exclude from default CI run via `pytest.ini`:

```ini
[pytest]
addopts = -m "not integration"
```

---

## Output Validation (`test_output.py`)

Run against the `data/` directory after a crawl to catch structural changes on the source site.

### Minimum paint count thresholds

Each medium file must contain at least a configured minimum number of paint entries. This catches cases where the site's HTML structure has changed and the crawler is silently returning empty or near-empty results.

Thresholds are defined in `tests/thresholds.json` and set after the first successful crawl:

```json
{
  "oils": 50,
  "acrylics": 50,
  "watercolors": 30
}
```

**Set thresholds after the first successful crawl.** Use ~80% of the initial count as the threshold to allow for natural variation (paints being added or removed from the source site).

### Additional output checks
- Every entry has `medium`, `brand`, `name`, `hex_available`, and `source_url`
- `hex` is either a string matching `#[0-9a-f]{6}` or `null`
- `hex_available` is `false` if and only if `hex` is `null`
- `source_url` starts with `http://www.art-paints.com`

---

## Definition of Done

A task is complete when:
- [ ] All unit tests pass (`pytest tests/` with no `-m` flags)
- [ ] Output validation passes against the latest `data/` files
- [ ] No new skipped entries are unexplained in the crawler log
- [ ] Integration test has been run manually at least once before a release
