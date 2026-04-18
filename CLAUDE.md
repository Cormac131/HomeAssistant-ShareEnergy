# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install test dependencies
python -m pip install -r requirements-test.txt

# Run unit tests (no network, no homeassistant required)
python -m pytest tests/test_parser.py -v

# Run live scrape tests (hits share-energy.com)
python -m pytest tests/test_live.py -v

# Skip live tests
SHARE_ENERGY_SKIP_LIVE=1 python -m pytest tests/ -v

# Run a single test
python -m pytest tests/test_parser.py::TestShareEV::test_day_rate_parsed -v
```

## Architecture

This is a Home Assistant HACS custom integration. HA loads `custom_components/share_energy/` as a package; the entry point is `__init__.py` → `coordinator.py` → `parser.py`.

**Separation of concerns:**
- `parser.py` — pure Python, no HA imports. Contains all scraping logic. Imported standalone by tests (via `conftest.py` `sys.path` manipulation) to avoid needing `homeassistant` installed.
- `coordinator.py` — wraps `parser.py` in a `DataUpdateCoordinator`, handles `aiohttp` fetch, runs `parse_page` in the executor.
- `sensor.py` — creates one `CoordinatorEntity` sensor per tariff/rate combination, driven entirely by `coordinator.data`.
- `const.py` — single source of truth for tariff definitions (`TARIFFS` dict), rate keys, labels, and units.

**Scraping approach:** The page (`https://share-energy.com/residential-tabs`) is server-side rendered. Prices live in `<div class="tab-pane ... pricing">` sections, one per tariff. Within each pane, `<li>` elements hold a `<b>` label (e.g. `"Day Rate"`, `"24 Hr Rate"`) and the Inc. VAT price as the second `<b>` tag. `_LABEL_MAP` in `parser.py` maps these page labels to internal rate keys. The site uses a self-signed cert chain; `ssl=False` is intentional in both `coordinator.py` and `test_live.py`.

**Adding a new tariff:** Add an entry to `TARIFFS` in `const.py` with its `search_text` (the exact heading text on the page), `name`, and `rates` list. No other files need changing.

**Tests:** `tests/conftest.py` adds `custom_components/share_energy/` directly to `sys.path` so `parser` and `const` are importable as top-level modules without triggering `__init__.py`. The fixture in `tests/fixtures.py` mirrors the real page's HTML structure — keep it in sync if the page structure changes.

**CI:** `.github/workflows/scrape_check.yml` runs daily at 08:00 UTC. On schedule failures it auto-opens a GitHub issue (with deduplication). Live tests are skipped on PRs (`SHARE_ENERGY_SKIP_LIVE=1`).
