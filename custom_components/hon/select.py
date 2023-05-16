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
from .hon import HonEntity, HonCoordinator, unique_entities

_LOGGER = logging.getLogger(__name__)

SELECTS = {
    "WM": (
        SelectEntityDescription(
            key="startProgram.spinSpeed",
            name="Spin speed",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:numeric",
            unit_of_measurement=REVOLUTIONS_PER_MINUTE,
            translation_key="spin_speed",
        ),
        SelectEntityDescription(
            key="startProgram.temp",
            name="Temperature",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:thermometer",
            unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="temperature",
        ),
        SelectEntityDescription(
            key="startProgram.program",
            name="Program",
            entity_category=EntityCategory.CONFIG,
            translation_key="programs_wm",
        ),
    ),
    "TD": (
        SelectEntityDescription(
            key="startProgram.program",
            name="Program",
            entity_category=EntityCategory.CONFIG,
            translation_key="programs_td",
        ),
        SelectEntityDescription(
            key="startProgram.dryTimeMM",
            name="Dry Time",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:timer",
            unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="dry_time",
        ),
        SelectEntityDescription(
            key="startProgram.dryLevel",
            name="Dry level",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:hair-dryer",
            translation_key="dry_levels",
        ),
    ),
    "OV": (
        SelectEntityDescription(
            key="startProgram.program",
            name="Program",
            entity_category=EntityCategory.CONFIG,
            translation_key="programs_ov",
        ),
    ),
    "IH": (
        SelectEntityDescription(
            key="startProgram.program",
            name="Program",
            entity_category=EntityCategory.CONFIG,
            translation_key="programs_ih",
        ),
    ),
    "DW": (
        SelectEntityDescription(
            key="startProgram.program",
            name="Program",
            entity_category=EntityCategory.CONFIG,
            translation_key="programs_dw",
        ),
        SelectEntityDescription(
            key="startProgram.temp",
            name="Temperature",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:thermometer",
            unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="temperature",
        ),
        SelectEntityDescription(
            key="startProgram.remainingTime",
            name="Remaining Time",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:timer",
            unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="remaining_time",
        ),
    ),
    "AC": (
        SelectEntityDescription(
            key="startProgram.program",
            name="Program",
            translation_key="programs_ac",
        ),
        SelectEntityDescription(
            key="settings.humanSensingStatus",
            name="Eco Pilot",
            icon="mdi:run",
            translation_key="eco_pilot",
        ),
    ),
    "REF": (
        SelectEntityDescription(
            key="startProgram.program",
            name="Program",
            entity_category=EntityCategory.CONFIG,
            translation_key="programs_ref",
        ),
    ),
}

SELECTS["WD"] = unique_entities(SELECTS["WM"], SELECTS["TD"])


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
                if description.key not in device.available_settings:
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

        if not (setting := self._device.settings.get(description.key)):
            self._attr_options: list[str] = []
        elif not isinstance(setting, HonParameterFixed):
            self._attr_options: list[str] = setting.values
        else:
            self._attr_options: list[str] = [setting.value]

    @property
    def current_option(self) -> str | None:
        value = self._device.settings.get(self.entity_description.key)
        if value is None or value.value not in self._attr_options:
            return None
        return value.value

    async def async_select_option(self, option: str) -> None:
        self._device.settings[self.entity_description.key].value = option
        if "settings." in self.entity_description.key:
            await self._device.commands["settings"].send()
        elif self._device.appliance_type in ["AC"]:
            await self._device.commands["startProgram"].send()
        await self.coordinator.async_refresh()

    @callback
    def _handle_coordinator_update(self):
        setting = self._device.settings.get(self.entity_description.key)
        if setting is None:
            self._attr_available = False
            self._attr_options: list[str] = []
            self._attr_native_value = None
        else:
            self._attr_available = True
            self._attr_options: list[str] = setting.values
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
