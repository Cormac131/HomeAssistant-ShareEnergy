"""Pure parsing logic — no Home Assistant imports, so this is unit-testable standalone."""
from __future__ import annotations

import logging
import re

from bs4 import BeautifulSoup

try:
    from .const import TARIFFS  # when loaded as part of the HA package
except ImportError:
    from const import TARIFFS   # when loaded standalone for tests

_LOGGER = logging.getLogger(__name__)

# Maps the bold label text on the page to our internal rate key.
# Matched case-insensitively after stripping whitespace.
_LABEL_MAP: dict[str, str] = {
    "24 hr rate": "unit_rate",
    "day rate": "day_rate",
    "night rate": "night_rate",
    "heat rate": "heat_rate",
    "heat": "heat_rate",  # keypad variant uses just "Heat"
    "standing charge": "standing_charge",
}


def _parse_pricing_pane(pane) -> dict[str, float | None]:
    """Extract {rate_key: inc_vat_price} from a pricing tab-pane element."""
    rates: dict[str, float | None] = {}
    for li in pane.find_all("li"):
        bold_tags = li.find_all("b")
        if len(bold_tags) < 2:
            continue
        label = bold_tags[0].get_text(strip=True).lower()
        rate_key = _LABEL_MAP.get(label)
        if rate_key is None:
            continue
        try:
            rates[rate_key] = float(bold_tags[1].get_text(strip=True))
        except (ValueError, IndexError):
            rates[rate_key] = None
    return rates


def parse_page(html: str) -> dict[str, dict[str, float | None]]:
    """Parse the Share Energy residential tariffs page into structured price data."""
    soup = BeautifulSoup(html, "html.parser")

    data: dict[str, dict[str, float | None]] = {}

    for tariff_key, cfg in TARIFFS.items():
        expected_rates = cfg["rates"]

        # Find the element containing the tariff name text
        name_node = soup.find(string=re.compile(re.escape(cfg["search_text"]), re.IGNORECASE))
        if name_node is None:
            _LOGGER.warning("Tariff '%s' not found on page", cfg["search_text"])
            data[tariff_key] = {r: None for r in expected_rates}
            continue

        # Walk up until we find a container that holds the pricing pane
        container = name_node.parent
        pricing_pane = None
        for _ in range(10):  # bound the search
            if container is None:
                break
            pricing_pane = container.find("div", class_=re.compile(r"\bpricing\b"))
            if pricing_pane is not None:
                break
            container = container.parent

        if pricing_pane is None:
            _LOGGER.warning("Pricing pane not found for '%s'", cfg["search_text"])
            data[tariff_key] = {r: None for r in expected_rates}
            continue

        found = _parse_pricing_pane(pricing_pane)
        _LOGGER.debug("Parsed %s: %s", tariff_key, found)

        data[tariff_key] = {r: found.get(r) for r in expected_rates}

    return data
