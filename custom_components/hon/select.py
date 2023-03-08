from __future__ import annotations

from pyhon import HonConnection
from pyhon.device import HonDevice
from pyhon.parameter import HonParameterFixed

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature, REVOLUTIONS_PER_MINUTE
from homeassistant.core import callback
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN
from .hon import HonEntity, HonCoordinator

SELECTS = {
    "WM": (
        SelectEntityDescription(
            key="startProgram.spinSpeed",
            name="Spin speed",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:numeric",
            unit_of_measurement=REVOLUTIONS_PER_MINUTE
        ),
        SelectEntityDescription(
            key="startProgram.temp",
            name="Temperature",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:thermometer",
            unit_of_measurement=UnitOfTemperature.CELSIUS
        ),
        SelectEntityDescription(
            key="startProgram.program",
            name="Programme",
            entity_category=EntityCategory.CONFIG
        ),
    )
}


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities) -> None:
    hon: HonConnection = hass.data[DOMAIN][entry.unique_id]
    coordinators = hass.data[DOMAIN]["coordinators"]
    appliances = []
    for device in hon.devices:
        if device.mac_address in coordinators:
            coordinator = hass.data[DOMAIN]["coordinators"][device.mac_address]
        else:
            coordinator = HonCoordinator(hass, device)
            hass.data[DOMAIN]["coordinators"][device.mac_address] = coordinator
        await coordinator.async_config_entry_first_refresh()

        if descriptions := SELECTS.get(device.appliance_type):
            for description in descriptions:
                if not device.get(description.key):
                    continue
                appliances.extend([
                    HonSelectEntity(hass, coordinator, entry, device, description)]
                )
    async_add_entities(appliances)


class HonSelectEntity(HonEntity, SelectEntity):
    def __init__(self, hass, coordinator, entry, device: HonDevice, description) -> None:
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
        if not isinstance(self._device.settings[self.entity_description.key], HonParameterFixed):
            self._attr_options: list[str] = setting.values
        else:
            self._attr_options = [setting.value]
        self._attr_native_value = setting.value
        self.async_write_ha_state()
