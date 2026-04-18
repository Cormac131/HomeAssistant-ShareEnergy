"""Sensor entities for Share Energy tariff prices."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, TARIFFS, RATE_LABELS, RATE_UNITS
from .coordinator import ShareEnergyCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: ShareEnergyCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        ShareEnergySensor(coordinator, tariff_key, rate_key)
        for tariff_key, tariff_cfg in TARIFFS.items()
        for rate_key in tariff_cfg["rates"]
    ]
    async_add_entities(entities)


class ShareEnergySensor(CoordinatorEntity, SensorEntity):
    """A sensor representing one rate for one Share Energy tariff."""

    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(
        self,
        coordinator: ShareEnergyCoordinator,
        tariff_key: str,
        rate_key: str,
    ) -> None:
        super().__init__(coordinator)
        self._tariff_key = tariff_key
        self._rate_key = rate_key

        tariff_name = TARIFFS[tariff_key]["name"]
        rate_label = RATE_LABELS[rate_key]

        self._attr_unique_id = f"share_energy_{tariff_key}_{rate_key}"
        self._attr_name = f"{tariff_name} {rate_label}"
        self._attr_native_unit_of_measurement = RATE_UNITS[rate_key]
        self._attr_icon = "mdi:lightning-bolt"

    @property
    def native_value(self) -> float | None:
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self._tariff_key, {}).get(self._rate_key)

    @property
    def extra_state_attributes(self) -> dict:
        return {
            "tariff": TARIFFS[self._tariff_key]["name"],
            "rate_type": RATE_LABELS[self._rate_key],
            "source": "share-energy.com",
        }
