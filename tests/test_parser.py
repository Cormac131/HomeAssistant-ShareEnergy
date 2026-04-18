"""Unit tests for the Share Energy HTML parser using a local fixture.

parser.py and const.py are imported as standalone modules (no homeassistant dependency)
via the sys.path manipulation in conftest.py.
"""
import pytest
import parser as share_parser  # custom_components/share_energy/parser.py
from tests.fixtures import MOCK_HTML


@pytest.fixture
def parsed():
    return share_parser.parse_page(MOCK_HTML)


class TestShare24Credit:
    def test_unit_rate_parsed(self, parsed):
        assert parsed["share_24_credit"]["unit_rate"] == 31.96

    def test_standing_charge_parsed(self, parsed):
        assert parsed["share_24_credit"]["standing_charge"] == 13.33


class TestShareEV:
    def test_day_rate_parsed(self, parsed):
        assert parsed["share_ev"]["day_rate"] == 32.04

    def test_night_rate_parsed(self, parsed):
        assert parsed["share_ev"]["night_rate"] == 15.56

    def test_standing_charge_parsed(self, parsed):
        assert parsed["share_ev"]["standing_charge"] == 13.33


class TestShareEco7:
    def test_day_rate_parsed(self, parsed):
        assert parsed["share_eco7"]["day_rate"] == 32.04

    def test_night_rate_parsed(self, parsed):
        assert parsed["share_eco7"]["night_rate"] == 15.56

    def test_heat_rate_parsed(self, parsed):
        assert parsed["share_eco7"]["heat_rate"] == 15.56

    def test_standing_charge_parsed(self, parsed):
        assert parsed["share_eco7"]["standing_charge"] == 13.33


class TestShare24Keypad:
    def test_unit_rate_parsed(self, parsed):
        assert parsed["share_24_keypad"]["unit_rate"] == 31.96

    def test_standing_charge_parsed(self, parsed):
        assert parsed["share_24_keypad"]["standing_charge"] == 16.67


class TestShareEco7Keypad:
    def test_day_rate_parsed(self, parsed):
        assert parsed["share_eco7_keypad"]["day_rate"] == 32.04

    def test_night_rate_parsed(self, parsed):
        assert parsed["share_eco7_keypad"]["night_rate"] == 15.56

    def test_standing_charge_parsed(self, parsed):
        assert parsed["share_eco7_keypad"]["standing_charge"] == 16.67


class TestMissingTariff:
    def test_missing_tariff_returns_none_values(self):
        data = share_parser.parse_page("<html><body>No tariffs here</body></html>")
        for tariff_key, values in data.items():
            for rate_key, value in values.items():
                assert value is None, f"{tariff_key}.{rate_key} should be None for empty page"


class TestPriceValidity:
    def test_all_rates_are_positive(self, parsed):
        for tariff_key, rates in parsed.items():
            for rate_key, value in rates.items():
                if value is not None:
                    assert value > 0, f"{tariff_key}.{rate_key} must be positive, got {value}"

    def test_no_unexpected_none_values(self, parsed):
        """Every expected rate should be found in the fixture."""
        for tariff_key, rates in parsed.items():
            for rate_key, value in rates.items():
                assert value is not None, (
                    f"{tariff_key}.{rate_key} was None — "
                    "parser failed to extract a price that should be present"
                )
