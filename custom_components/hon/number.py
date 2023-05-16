from __future__ import annotations

from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime, UnitOfTemperature
from homeassistant.core import callback
from homeassistant.helpers.entity import EntityCategory
from pyhon import Hon
from pyhon.parameter.base import HonParameter
from pyhon.parameter.fixed import HonParameterFixed
from pyhon.parameter.range import HonParameterRange

from .const import DOMAIN
from .hon import HonEntity, HonCoordinator, unique_entities

NUMBERS: dict[str, tuple[NumberEntityDescription, ...]] = {
    "WM": (
        NumberEntityDescription(
            key="startProgram.delayTime",
            name="Delay Time",
            icon="mdi:timer-plus",
            entity_category=EntityCategory.CONFIG,
            native_unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="delay_time",
        ),
        NumberEntityDescription(
            key="startProgram.rinseIterations",
            name="Rinse Iterations",
            icon="mdi:rotate-right",
            entity_category=EntityCategory.CONFIG,
            translation_key="rinse_iterations",
        ),
        NumberEntityDescription(
            key="startProgram.mainWashTime",
            name="Main Wash Time",
            icon="mdi:clock-start",
            entity_category=EntityCategory.CONFIG,
            native_unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="wash_time",
        ),
        NumberEntityDescription(
            key="startProgram.steamLevel",
            name="Steam Level",
            icon="mdi:weather-dust",
            entity_category=EntityCategory.CONFIG,
            translation_key="steam_level",
        ),
        NumberEntityDescription(
            key="startProgram.waterHard",
            name="Water hard",
            icon="mdi:water",
            entity_category=EntityCategory.CONFIG,
            translation_key="water_hard",
        ),
        NumberEntityDescription(
            key="startProgram.lang",
            name="lang",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    "TD": (
        NumberEntityDescription(
            key="startProgram.delayTime",
            name="Delay time",
            icon="mdi:timer-plus",
            entity_category=EntityCategory.CONFIG,
            native_unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="delay_time",
        ),
        NumberEntityDescription(
            key="startProgram.tempLevel",
            name="Temperature level",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:thermometer",
            translation_key="tumbledryertemplevel",
        ),
        NumberEntityDescription(
            key="startProgram.dryTime",
            name="Dry Time",
            entity_category=EntityCategory.CONFIG,
            translation_key="dry_time",
        ),
    ),
    "OV": (
        NumberEntityDescription(
            key="startProgram.delayTime",
            name="Delay time",
            icon="mdi:timer-plus",
            entity_category=EntityCategory.CONFIG,
            native_unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="delay_time",
        ),
        NumberEntityDescription(
            key="startProgram.tempSel",
            name="Target Temperature",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:thermometer",
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="target_temperature",
        ),
        NumberEntityDescription(
            key="startProgram.prTime",
            name="Program Duration",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:timelapse",
            native_unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="program_duration",
        ),
    ),
    "IH": (
        NumberEntityDescription(
            key="startProgram.temp",
            name="Temperature",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:thermometer",
            translation_key="temperature",
        ),
        NumberEntityDescription(
            key="startProgram.powerManagement",
            name="Power Management",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:timelapse",
            translation_key="power_management",
        ),
    ),
    "DW": (
        NumberEntityDescription(
            key="startProgram.delayTime",
            name="Delay time",
            icon="mdi:timer-plus",
            entity_category=EntityCategory.CONFIG,
            native_unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="delay_time",
        ),
        NumberEntityDescription(
            key="startProgram.waterHard",
            name="Water hard",
            icon="mdi:water",
            entity_category=EntityCategory.CONFIG,
            translation_key="water_hard",
        ),
    ),
    "AC": (
        NumberEntityDescription(
            key="settings.tempSel",
            name="Target Temperature",
            icon="mdi:thermometer",
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="target_temperature",
        ),
    ),
    "REF": (
        NumberEntityDescription(
            key="settings.tempSelZ1",
            name="Fridge Temperature",
            icon="mdi:thermometer",
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="fridge_temp_sel",
        ),
        NumberEntityDescription(
            key="settings.tempSelZ2",
            name="Freezer Temperature",
            icon="mdi:thermometer",
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="freezer_temp_sel",
        ),
    ),
}

NUMBERS["WD"] = unique_entities(NUMBERS["WM"], NUMBERS["TD"])


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

        if descriptions := NUMBERS.get(device.appliance_type):
            for description in descriptions:
                if description.key not in device.available_settings:
                    continue
                appliances.extend(
                    [HonNumberEntity(hass, coordinator, entry, device, description)]
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
        setting = self._device.settings[self.entity_description.key]
        if not (
            isinstance(setting, HonParameter) or isinstance(setting, HonParameterFixed)
        ):
            setting.value = value
        if "settings." in self.entity_description.key:
            await self._device.commands["settings"].send()
        await self.coordinator.async_refresh()

    @callback
    def _handle_coordinator_update(self):
        setting = self._device.settings[self.entity_description.key]
        if isinstance(setting, HonParameterRange):
            self._attr_native_max_value = setting.max
            self._attr_native_min_value = setting.min
            self._attr_native_step = setting.step
        self._attr_native_value = setting.value
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if self.entity_category == EntityCategory.CONFIG:
            return super().available
        else:
            return (
                super().available
                and self._device.get("remoteCtrValid", "1") == "1"
                and self._device.get("attributes.lastConnEvent.category")
                != "DISCONNECTED"
            )
