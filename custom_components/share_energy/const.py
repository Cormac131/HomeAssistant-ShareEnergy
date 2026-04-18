DOMAIN = "share_energy"
SCRAPE_URL = "https://share-energy.com/residential-tabs"
DEFAULT_SCAN_INTERVAL = 3600  # 1 hour

TARIFFS = {
    "share_24_credit": {
        "name": "Share 24 Credit",
        "search_text": "Share 24 Credit",
        "rates": ["unit_rate", "standing_charge"],
    },
    "share_ev": {
        "name": "Share EV",
        "search_text": "Share EV",
        "rates": ["day_rate", "night_rate", "standing_charge"],
    },
    "share_eco7": {
        "name": "Share Eco 7",
        "search_text": "Share Eco 7",
        "rates": ["day_rate", "night_rate", "heat_rate", "standing_charge"],
    },
    "share_24_keypad": {
        "name": "Share 24 Keypad",
        "search_text": "Share 24 Keypad",
        "rates": ["unit_rate", "standing_charge"],
    },
    "share_eco7_keypad": {
        "name": "Share Eco 7 Keypad",
        "search_text": "Share Eco 7 Keypad",
        "rates": ["day_rate", "night_rate", "standing_charge"],
    },
}

RATE_LABELS = {
    "unit_rate": "Unit Rate",
    "day_rate": "Day Rate",
    "night_rate": "Night Rate",
    "heat_rate": "Heat Rate",
    "standing_charge": "Standing Charge",
}

RATE_UNITS = {
    "unit_rate": "p/kWh",
    "day_rate": "p/kWh",
    "night_rate": "p/kWh",
    "heat_rate": "p/kWh",
    "standing_charge": "p/day",
}
