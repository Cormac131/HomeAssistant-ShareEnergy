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


class TestRobustness:
    """Verify the parser never raises — it always returns a complete dict with float-or-None
    values regardless of what the page contains. HA marks sensors unavailable when
    native_value is None, so None is always safe; an exception is not."""

    def test_empty_string_does_not_raise(self):
        data = share_parser.parse_page("")
        assert isinstance(data, dict)

    def test_malformed_html_does_not_raise(self):
        data = share_parser.parse_page("<html><div><p><<broken>>")
        assert isinstance(data, dict)

    def test_truncated_html_does_not_raise(self):
        from tests.fixtures import MOCK_HTML
        data = share_parser.parse_page(MOCK_HTML[:200])
        assert isinstance(data, dict)

    def test_section_present_but_no_pricing_pane(self):
        html = "<html><body><h3>Share 24 Credit</h3><div>no pricing here</div></body></html>"
        data = share_parser.parse_page(html)
        assert isinstance(data, dict)
        for value in data["share_24_credit"].values():
            assert value is None

    def test_garbled_price_text_returns_none_not_exception(self):
        html = """<html><body>
        <h3>Share 24 Credit</h3>
        <div class="tab-pane fade show active pricing">
          <ul><li><p><b>24 Hr Rate</b><br/><b>TBC</b> pence per KWh</p></li></ul>
        </div></body></html>"""
        data = share_parser.parse_page(html)
        assert isinstance(data, dict)
        assert data["share_24_credit"]["unit_rate"] is None

    def test_return_value_always_contains_all_tariff_keys(self):
        data = share_parser.parse_page("")
        import const as share_const
        assert set(data.keys()) == set(share_const.TARIFFS.keys())

    def test_return_value_always_contains_all_rate_keys(self):
        data = share_parser.parse_page("")
        import const as share_const
        for tariff_key, cfg in share_const.TARIFFS.items():
            assert set(data[tariff_key].keys()) == set(cfg["rates"])

    def test_all_values_are_float_or_none(self):
        from tests.fixtures import MOCK_HTML
        data = share_parser.parse_page(MOCK_HTML)
        for tariff_key, rates in data.items():
            for rate_key, value in rates.items():
                assert value is None or isinstance(value, float), (
                    f"{tariff_key}.{rate_key} = {value!r} is neither float nor None"
                )


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
