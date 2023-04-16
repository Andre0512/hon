from __future__ import annotations

import logging

from pyhon import Hon
from pyhon.appliance import HonAppliance
from pyhon.parameter.fixed import HonParameterFixed

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature, UnitOfTime, REVOLUTIONS_PER_MINUTE
from homeassistant.core import callback
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN
from .hon import HonEntity, HonCoordinator

_LOGGER = logging.getLogger(__name__)

SELECTS = {
    "WM": (
        SelectEntityDescription(
            key="startProgram.spinSpeed",
            name="Spin speed",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:numeric",
            unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        ),
        SelectEntityDescription(
            key="startProgram.temp",
            name="Temperature",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:thermometer",
            unit_of_measurement=UnitOfTemperature.CELSIUS,
        ),
        SelectEntityDescription(
            key="startProgram.program",
            name="Program",
            entity_category=EntityCategory.CONFIG,
            translation_key="programs",
        ),
    ),
    "TD": (
        SelectEntityDescription(
            key="startProgram.program",
            name="Program",
            entity_category=EntityCategory.CONFIG,
            translation_key="programs",
        ),
        SelectEntityDescription(
            key="startProgram.dryTimeMM",
            name="Time",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:timer",
            unit_of_measurement=UnitOfTime.MINUTES,
        ),
    ),
    "WD": (
        SelectEntityDescription(
            key="startProgram.program",
            name="Program",
            entity_category=EntityCategory.CONFIG,
            translation_key="programs",
        ),
    ),
    "OV": (
        SelectEntityDescription(
            key="startProgram.program",
            name="Program",
            entity_category=EntityCategory.CONFIG,
            translation_key="programs",
        ),
        SelectEntityDescription(
            key="startProgram.preheatStatus",
            name="Preheat",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    "IH": (
        SelectEntityDescription(
            key="startProgram.program",
            name="Program",
            entity_category=EntityCategory.CONFIG,
            translation_key="programs",
        ),
    ),
}


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities) -> None:
    hon: Hon = hass.data[DOMAIN][entry.unique_id]
    coordinators = hass.data[DOMAIN]["coordinators"]
    appliances = []
    for device in hon.appliances:
        if device.unique_id in coordinators:
            coordinator = hass.data[DOMAIN]["coordinators"][device.unique_id]
        else:
            coordinator = HonCoordinator(hass, device)
            hass.data[DOMAIN]["coordinators"][device.unique_id] = coordinator
        await coordinator.async_config_entry_first_refresh()

        if descriptions := SELECTS.get(device.appliance_type):
            for description in descriptions:
                if not device.settings.get(description.key):
                    continue
                appliances.extend(
                    [HonSelectEntity(hass, coordinator, entry, device, description)]
                )
    async_add_entities(appliances)


class HonSelectEntity(HonEntity, SelectEntity):
    def __init__(
        self, hass, coordinator, entry, device: HonAppliance, description
    ) -> None:
        super().__init__(hass, entry, coordinator, device)

        self._coordinator = coordinator
        self._device = device
        self.entity_description = description
        self._attr_unique_id = f"{super().unique_id}{description.key}"

        if not isinstance(self._device.settings[description.key], HonParameterFixed):
            self._attr_options: list[str] = device.settings[description.key].values
        else:
            self._attr_options: list[str] = [device.settings[description.key].value]

    @property
    def current_option(self) -> str | None:
        value = self._device.settings[self.entity_description.key].value
        if value is None or value not in self._attr_options:
            return None
        return value

    async def async_select_option(self, option: str) -> None:
        self._device.settings[self.entity_description.key].value = option
        await self.coordinator.async_request_refresh()

    @callback
    def _handle_coordinator_update(self):
        setting = self._device.settings[self.entity_description.key]
        if not isinstance(
            self._device.settings[self.entity_description.key], HonParameterFixed
        ):
            self._attr_options: list[str] = setting.values
        else:
            self._attr_options = [setting.value]
        self._attr_native_value = setting.value
        self.async_write_ha_state()
