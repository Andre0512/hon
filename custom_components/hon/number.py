from __future__ import annotations

from pyhon import HonConnection
from pyhon.parameter import HonParameterRange

from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime, UnitOfTemperature
from homeassistant.core import callback
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN
from .hon import HonEntity, HonCoordinator

NUMBERS: dict[str, tuple[NumberEntityDescription, ...]] = {
    "WM": (
        NumberEntityDescription(
            key="startProgram.delayTime",
            name="Delay Time",
            icon="mdi:timer-plus",
            entity_category=EntityCategory.CONFIG,
            native_unit_of_measurement=UnitOfTime.MINUTES
        ),
        NumberEntityDescription(
            key="startProgram.rinseIterations",
            name="Rinse Iterations",
            icon="mdi:rotate-right",
            entity_category=EntityCategory.CONFIG
        ),
        NumberEntityDescription(
            key="startProgram.mainWashTime",
            name="Main Wash Time",
            icon="mdi:clock-start",
            entity_category=EntityCategory.CONFIG,
            native_unit_of_measurement=UnitOfTime.MINUTES
        ),
    ),
    "TD": (
        NumberEntityDescription(
            key="startProgram.delayTime",
            name="Delay time",
            icon="mdi:timer-plus",
            entity_category=EntityCategory.CONFIG,
            native_unit_of_measurement=UnitOfTime.MINUTES
        ),
        NumberEntityDescription(
            key="startProgram.dryLevel",
            name="Dry level",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:hair-dryer",
            translation_key="tumbledryerdrylevel"
        ),
        NumberEntityDescription(
            key="startProgram.tempLevel",
            name="Temperature level",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:thermometer",
            translation_key="tumbledryertemplevel"
        ),
        NumberEntityDescription(
            key="startProgram.antiCreaseTime",
            name="Anti-Crease time",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:timer",
            native_unit_of_measurement=UnitOfTime.MINUTES
        ),
        NumberEntityDescription(
            key="startProgram.sterilizationStatus",
            name="Sterilization status",
            icon="mdi:clock-start",
            entity_category=EntityCategory.CONFIG
        ),
    ),
    "WD": (
        NumberEntityDescription(
            key="startProgram.delayTime",
            name="Delay Time",
            icon="mdi:timer-plus",
            entity_category=EntityCategory.CONFIG,
            native_unit_of_measurement=UnitOfTime.MINUTES
        ),
    ),
    "OV": (
        NumberEntityDescription(
            key="startProgram.delayTime",
            name="Delay time",
            icon="mdi:timer-plus",
            entity_category=EntityCategory.CONFIG,
            native_unit_of_measurement=UnitOfTime.MINUTES
        ),
        NumberEntityDescription(
            key="startProgram.tempSel",
            name="Target Temperature",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:thermometer",
            native_unit_of_measurement=UnitOfTemperature.CELSIUS
        ),

        NumberEntityDescription(
            key="startProgram.prTime",
            name="Program Duration",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:timelapse",
            native_unit_of_measurement=UnitOfTime.MINUTES
        ),
    ),
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

        if descriptions := NUMBERS.get(device.appliance_type):
            for description in descriptions:
                appliances.extend([
                    HonNumberEntity(hass, coordinator, entry, device, description)]
                )

    async_add_entities(appliances)


class HonNumberEntity(HonEntity, NumberEntity):
    def __init__(self, hass, coordinator, entry, device, description) -> None:
        super().__init__(hass, entry, coordinator, device)

        self._coordinator = coordinator
        self._device = device
        self._data = device.settings[description.key]
        self.entity_description = description
        self._attr_unique_id = f"{super().unique_id}{description.key}"

        if isinstance(self._data, HonParameterRange):
            self._attr_native_max_value = self._data.max
            self._attr_native_min_value = self._data.min
            self._attr_native_step = self._data.step

    @property
    def native_value(self) -> float | None:
        return self._device.get(self.entity_description.key)

    async def async_set_native_value(self, value: float) -> None:
        self._device.settings[self.entity_description.key].value = value
        await self.coordinator.async_request_refresh()

    @callback
    def _handle_coordinator_update(self):
        setting = self._device.settings[self.entity_description.key]
        if isinstance(setting, HonParameterRange):
            self._attr_native_max_value = setting.max
            self._attr_native_min_value = setting.min
            self._attr_native_step = setting.step
        self._attr_native_value = setting.value
        self.async_write_ha_state()
