# Security & Privacy — paint-crawl

## Summary

paint-crawl collects no user data. It fetches publicly available paint information from a third-party website and stores it as JSON files in a private repository. The attack surface is minimal by design.

---

## Credentials & Secrets

- **No API keys or secrets required.** art-paints.com requires no authentication.
- **GitHub Actions** uses the built-in `GITHUB_TOKEN` for committing data files back to the repo. No personal access tokens or external credentials are needed.
- `.env` files and any secret-like files must be in `.gitignore`. The crawler should never read from environment variables that contain credentials.

---

## External Requests

The crawler makes outbound HTTP requests to `art-paints.com` only.

- `robots.txt` is checked before crawling begins (see `BUSINESS_LOGIC.md`).
- Requests are rate-limited to one every 2 seconds to avoid overloading the source server.
- No data is sent to the source site beyond standard HTTP GET requests (no POST, no form submissions, no cookies).
- The crawler does not follow redirects to external domains.

---

## Data Stored

Only publicly available paint data is stored:

| Field | Sensitivity |
|---|---|
| `medium` | None — public category |
| `brand` | None — public manufacturer name |
| `name` | None — public color name |
| `hex` | None — publicly listed color value |
| `source_url` | None — public URL |
| `crawled_at` | None — internal timestamp |

No personally identifiable information (PII) is collected or stored at any point.

---

## Repository

- The repository is **private**. JSON output files are committed to the repo and are not publicly accessible.
- The `GITHUB_TOKEN` used in Actions has repository-scoped write access only. It cannot access other repositories or organization resources.

---

## Dependency Risk

Dependencies (`requests`, `beautifulsoup4`) are well-maintained, widely used libraries with no known credential-handling concerns. Pin dependency versions in `requirements.txt` to avoid unexpected updates pulling in vulnerabilities.

---

## What This Project Does NOT Do

- No user accounts, authentication, or sessions
- No analytics or telemetry
- No data sent to third parties beyond the crawl target
- No public API or web interface
