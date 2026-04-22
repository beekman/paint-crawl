# Business Logic — paint-crawl

## Hex Value Normalization

### Storage format
All hex values are stored lowercase with a `#` prefix: `#e32636`.

### Conversion rules (applied in order)

| Input format | Action |
|---|---|
| 6-digit hex (`#E32636`, `E32636`) | Normalize to lowercase `#e32636` |
| 3-digit hex (`#e36`) | Expand to 6-digit `#ee3366`, then lowercase |
| RGB (`rgb(227, 38, 54)`) | Convert to hex, then lowercase |
| HSL (`hsl(354, 74%, 52%)`) | Convert to hex, then lowercase |
| Named CSS color (`crimson`) | Convert to hex equivalent, then lowercase |
| Unrecognizable / unparseable | Set `hex: null`, `hex_available: false` |

### Validation
After conversion, validate that the result matches `#[0-9a-f]{6}`. If it doesn't, treat as unrecognizable.

---

## Duplicate Handling

A duplicate is defined as two entries with the same `(medium, brand, name)` combination (case-insensitive comparison).

**Rule:** Keep the first entry that has a valid hex value (`hex_available: true`). If no entry in the duplicate set has a valid hex value, keep the first entry encountered.

---

## Rate Limiting

- Wait **2 seconds** between each HTTP request.
- Applied globally — between all requests, not just between pages of the same medium.
- If a request fails with a 429 (Too Many Requests) or 503, wait 30 seconds and retry once. If it fails again, skip and log.

---

## robots.txt

Before crawling begins, fetch and parse `http://www.art-paints.com/robots.txt`.

- If crawling the target paths is disallowed, **stop and log a warning** — do not proceed.
- If `robots.txt` is unreachable (404, timeout), log a warning and proceed.

---

## Missing or Empty Fields

| Field | If missing or empty |
|---|---|
| `brand` | Skip the entry and log it |
| `name` | Skip the entry and log it |
| `hex` | Set `hex: null`, `hex_available: false` — do not skip |
| `source_url` | Set to the parent page URL as a fallback |

---

## Text Normalization

- **Brand and name:** Trim leading/trailing whitespace. Preserve original casing as found on the source site.
- **Medium:** Stored as a lowercase slug matching the output filename (e.g., `"oils"`, `"acrylics"`). Derived from the medium page URL or heading, not hardcoded.

---

## Logging

The crawler logs the following to stdout:
- Each medium being crawled
- Number of paints found per medium
- Entries skipped (reason: missing field, unrecognizable color, duplicate)
- robots.txt check result
- Any HTTP errors encountered
