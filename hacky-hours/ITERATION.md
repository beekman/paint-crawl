# Iteration — v0.1.0 → V1

## Captured

No bugs or feedback to report from v0.1.0.

V1 work identified from roadmap:

- **Retry logic (429/503)** — already implemented during MVP. `fetch()` in crawler.py
  does a 30s wait + single retry before skipping and logging. No action needed.

- **GitHub Actions workflow** — `.github/workflows/crawl.yml` with weekly schedule
  and manual dispatch. Commits updated data files to the repo.

- **Integration tests** — `tests/test_integration.py` already exists with tests marked
  `@pytest.mark.integration`, excluded from default CI. Verified structure is correct.
  No additional work needed.

## Triage

| Item | Category | Action |
|------|----------|--------|
| Retry logic | ✓ Done | No action |
| GitHub Actions workflow | Next milestone (V1) | Add to backlog |
| Integration tests | ✓ Done | No action |

## Design docs to amend

- `ARCHITECTURE.md` — add the GitHub Actions workflow once implemented
- `BUSINESS_LOGIC.md` — already documents retry logic correctly ✓
