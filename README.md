# Share Energy – Home Assistant Integration

<img src="images/logo.png" alt="Share Energy logo" width="100" align="right"/>

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

A HACS custom integration that scrapes live energy tariff prices from [share-energy.com](https://share-energy.com/residential-tabs) and exposes them as Home Assistant sensor entities.

## Sensors created

| Entity | Description | Unit |
|--------|-------------|------|
| `sensor.share_24_credit_unit_rate` | Share 24 Credit unit rate | p/kWh |
| `sensor.share_24_credit_standing_charge` | Share 24 Credit standing charge | p/day |
| `sensor.share_ev_day_rate` | Share EV day rate | p/kWh |
| `sensor.share_ev_night_rate` | Share EV night rate | p/kWh |
| `sensor.share_ev_standing_charge` | Share EV standing charge | p/day |
| `sensor.share_eco_7_day_rate` | Share Eco 7 day rate | p/kWh |
| `sensor.share_eco_7_night_rate` | Share Eco 7 night rate | p/kWh |
| `sensor.share_eco_7_heat_rate` | Share Eco 7 heat rate | p/kWh |
| `sensor.share_eco_7_standing_charge` | Share Eco 7 standing charge | p/day |
| `sensor.share_24_keypad_unit_rate` | Share 24 Keypad unit rate | p/kWh |
| `sensor.share_24_keypad_standing_charge` | Share 24 Keypad standing charge | p/day |
| `sensor.share_eco_7_keypad_day_rate` | Share Eco 7 Keypad day rate | p/kWh |
| `sensor.share_eco_7_keypad_night_rate` | Share Eco 7 Keypad night rate | p/kWh |
| `sensor.share_eco_7_keypad_standing_charge` | Share Eco 7 Keypad standing charge | p/day |

All prices are **inc. VAT** as shown on the website. Prices refresh every hour.

## Installation via HACS

1. In HACS, go to **Integrations → Custom repositories**
2. Add `https://github.com/Cormac131/HomeAssistant-ShareEnergy` with category **Integration**
3. Install **Share Energy** from the HACS store
4. Restart Home Assistant
5. Go to **Settings → Devices & Services → Add Integration** and search for **Share Energy**

## Manual installation

1. Copy `custom_components/share_energy/` into your HA `config/custom_components/` directory
2. Restart Home Assistant
3. Add the integration via the UI as above
