# Product Overview — paint-crawl

## Who
The primary user is the developer (Ben), building data to feed into a separate paint mixing app. End users of the mixing app benefit indirectly — they get accurate commercial paint presets without manual color entry.

## What
A web crawler that scrapes [art-paints.com](http://www.art-paints.com/Paints/Art-Paints.html) to extract commercially available paint data, normalizes it, and outputs structured JSON files as importable palette presets.

Data captured per paint:
- Paint type (medium: oils, acrylics, watercolors, etc.)
- Brand / manufacturer
- Color name
- Hex value

Output: JSON files committed to this repo, consumable by the paint mixing app.

## Where
- CLI tool run locally or on a schedule via GitHub Actions
- No server, no public API — internal tooling only

## When
- MVP: crawler + normalized JSON output covering all mediums on art-paints.com
- V1: filtering and search capabilities for the mixing app to query the dataset

## Why
Paint mixing apps need accurate data about commercially available paints. Without it, users must manually look up and convert real-world paint colors to hex values — a tedious, error-prone process. paint-crawl bridges the physical-to-digital gap by maintaining an up-to-date, structured library of real paint colors.

## Constraints & Values

### Licensing
Private repository. Not open source. Not for sale — internal tooling only.

### Privacy
No user data collected. This tool only fetches and stores publicly available paint data from art-paints.com. No authentication, no user accounts, no analytics.

### Infrastructure
Free tier only. GitHub Actions for scheduled runs. JSON files committed to the repo as the data store. No managed database for MVP — filtering/search deferred to V1.

### Dependencies
Prefer minimal. Fewer moving parts = easier to maintain.
