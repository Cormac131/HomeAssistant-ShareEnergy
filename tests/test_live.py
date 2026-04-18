"""Live scrape test — hits share-energy.com and verifies all tariff prices are found.

Run with: pytest tests/test_live.py -v
Skipped automatically if SHARE_ENERGY_SKIP_LIVE=1 is set.
"""
import os
import pytest
import aiohttp
import asyncio

import parser as share_parser  # custom_components/share_energy/parser.py via conftest.py sys.path
import const as share_const    # custom_components/share_energy/const.py via conftest.py sys.path

SKIP_LIVE = os.getenv("SHARE_ENERGY_SKIP_LIVE", "0") == "1"


async def _fetch_and_parse() -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(share_const.SCRAPE_URL, timeout=aiohttp.ClientTimeout(total=30), ssl=False) as resp:
            resp.raise_for_status()
            html = await resp.text()
    return share_parser.parse_page(html)


@pytest.fixture(scope="module")
def live_data():
    return asyncio.run(_fetch_and_parse())


@pytest.mark.skipif(SKIP_LIVE, reason="SHARE_ENERGY_SKIP_LIVE is set")
class TestLiveScrape:
    """Fail loudly if the website has changed and prices can no longer be scraped."""

    @pytest.mark.parametrize("tariff_key,rate_key", [
        ("share_24_credit", "unit_rate"),
        ("share_24_credit", "standing_charge"),
        ("share_ev", "day_rate"),
        ("share_ev", "night_rate"),
        ("share_ev", "standing_charge"),
        ("share_eco7", "day_rate"),
        ("share_eco7", "night_rate"),
        ("share_eco7", "heat_rate"),
        ("share_eco7", "standing_charge"),
        ("share_24_keypad", "unit_rate"),
        ("share_24_keypad", "standing_charge"),
        ("share_eco7_keypad", "day_rate"),
        ("share_eco7_keypad", "night_rate"),
        ("share_eco7_keypad", "standing_charge"),
    ])
    def test_rate_is_scraped(self, live_data, tariff_key, rate_key):
        value = live_data.get(tariff_key, {}).get(rate_key)
        assert value is not None, (
            f"SCRAPE FAILURE: {tariff_key}.{rate_key} returned None.\n"
            f"The Share Energy website structure may have changed at {share_const.SCRAPE_URL}.\n"
            "Check parser.py regex patterns."
        )
        assert isinstance(value, float), f"{tariff_key}.{rate_key} should be a float, got {type(value)}"
        assert value > 0, f"{tariff_key}.{rate_key} = {value} is not a positive number"

    def test_unit_rates_are_plausible(self, live_data):
        """kWh prices should be between 1p and 100p."""
        for tariff_key, rate_key in [
            ("share_24_credit", "unit_rate"),
            ("share_ev", "day_rate"),
            ("share_ev", "night_rate"),
            ("share_eco7", "day_rate"),
            ("share_eco7", "night_rate"),
        ]:
            value = live_data.get(tariff_key, {}).get(rate_key)
            if value is not None:
                assert 1.0 <= value <= 100.0, (
                    f"{tariff_key}.{rate_key} = {value}p/kWh is outside plausible range 1–100p"
                )

    def test_standing_charges_are_plausible(self, live_data):
        """Standing charges should be between 1p and 100p/day."""
        for tariff_key, rate_key in [
            ("share_24_credit", "standing_charge"),
            ("share_ev", "standing_charge"),
            ("share_eco7", "standing_charge"),
            ("share_24_keypad", "standing_charge"),
            ("share_eco7_keypad", "standing_charge"),
        ]:
            value = live_data.get(tariff_key, {}).get(rate_key)
            if value is not None:
                assert 1.0 <= value <= 100.0, (
                    f"{tariff_key}.{rate_key} = {value}p/day is outside plausible range 1–100p"
                )
