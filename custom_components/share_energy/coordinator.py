"""Data coordinator: fetches and parses Share Energy tariff prices."""
from __future__ import annotations

import logging
from datetime import timedelta

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, SCRAPE_URL, DEFAULT_SCAN_INTERVAL
from .parser import parse_page

_LOGGER = logging.getLogger(__name__)


class ShareEnergyCoordinator(DataUpdateCoordinator):
    """Coordinator that scrapes share-energy.com for tariff prices."""

    def __init__(self, hass: HomeAssistant) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> dict[str, dict[str, float | None]]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(SCRAPE_URL, timeout=aiohttp.ClientTimeout(total=30), ssl=False) as resp:
                    resp.raise_for_status()
                    html = await resp.text()
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error fetching Share Energy page: {err}") from err

        return await self.hass.async_add_executor_job(parse_page, html)
