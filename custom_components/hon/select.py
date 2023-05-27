from __future__ import annotations

import logging
from dataclasses import dataclass

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature, UnitOfTime, REVOLUTIONS_PER_MINUTE
from homeassistant.core import callback
from homeassistant.helpers.entity import EntityCategory, Entity
from pyhon.appliance import HonAppliance
from pyhon.parameter.fixed import HonParameterFixed

from .const import DOMAIN
from .hon import HonEntity, unique_entities

_LOGGER = logging.getLogger(__name__)


@dataclass
class HonSelectEntityDescription(SelectEntityDescription):
    pass


@dataclass
class HonConfigSelectEntityDescription(SelectEntityDescription):
    entity_category: EntityCategory = EntityCategory.CONFIG


SELECTS = {
    "WM": (
        HonConfigSelectEntityDescription(
            key="startProgram.spinSpeed",
            name="Spin speed",
            icon="mdi:numeric",
            unit_of_measurement=REVOLUTIONS_PER_MINUTE,
            translation_key="spin_speed",
        ),
        HonConfigSelectEntityDescription(
            key="startProgram.temp",
            name="Temperature",
            icon="mdi:thermometer",
            unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="temperature",
        ),
        HonConfigSelectEntityDescription(
            key="startProgram.program",
            name="Program",
            translation_key="programs_wm",
        ),
    ),
    "TD": (
        HonConfigSelectEntityDescription(
            key="startProgram.program",
            name="Program",
            translation_key="programs_td",
        ),
        HonConfigSelectEntityDescription(
            key="startProgram.dryTimeMM",
            name="Dry Time",
            icon="mdi:timer",
            unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="dry_time",
        ),
        HonConfigSelectEntityDescription(
            key="startProgram.dryLevel",
            name="Dry level",
            icon="mdi:hair-dryer",
            translation_key="dry_levels",
        ),
    ),
    "OV": (
        HonConfigSelectEntityDescription(
            key="startProgram.program",
            name="Program",
            translation_key="programs_ov",
        ),
    ),
    "IH": (
        HonConfigSelectEntityDescription(
            key="startProgram.program",
            name="Program",
            translation_key="programs_ih",
        ),
    ),
    "DW": (
        HonConfigSelectEntityDescription(
            key="startProgram.program",
            name="Program",
            translation_key="programs_dw",
        ),
        HonConfigSelectEntityDescription(
            key="startProgram.temp",
            name="Temperature",
            icon="mdi:thermometer",
            unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="temperature",
        ),
        HonConfigSelectEntityDescription(
            key="startProgram.remainingTime",
            name="Remaining Time",
            icon="mdi:timer",
            unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="remaining_time",
        ),
    ),
    "AC": (
        HonSelectEntityDescription(
            key="startProgram.program",
            name="Program",
            translation_key="programs_ac",
        ),
        HonSelectEntityDescription(
            key="settings.humanSensingStatus",
            name="Eco Pilot",
            icon="mdi:run",
            translation_key="eco_pilot",
        ),
    ),
    "REF": (
        HonConfigSelectEntityDescription(
            key="startProgram.program",
            name="Program",
            translation_key="programs_ref",
        ),
        HonConfigSelectEntityDescription(
            key="startProgram.zone",
            name="Zone",
            icon="mdi:radiobox-marked",
            translation_key="ref_zones",
        ),
    ),
}

SELECTS["WD"] = unique_entities(SELECTS["WM"], SELECTS["TD"])


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities) -> None:
    entities = []
    for device in hass.data[DOMAIN][entry.unique_id].appliances:
        for description in SELECTS.get(device.appliance_type, []):
            if description.key not in device.available_settings:
                continue
            if isinstance(description, HonSelectEntityDescription):
                entity = HonSelectEntity(hass, entry, device, description)
            elif isinstance(description, HonConfigSelectEntityDescription):
                entity = HonConfigSelectEntity(hass, entry, device, description)
            else:
                continue
            await entity.coordinator.async_config_entry_first_refresh()
            entities.append(entity)
    async_add_entities(entities)


class HonSelectEntity(HonEntity, SelectEntity):
    entity_description: HonSelectEntityDescription

    def __init__(self, hass, entry, device: HonAppliance, description) -> None:
        super().__init__(hass, entry, device, description)

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
        command = self.entity_description.key.split(".")[0]
        await self._device.commands[command].send()
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
        return (
            super().available
            and self._device.get("remoteCtrValid", "1") == "1"
            and self._device.get("attributes.lastConnEvent.category") != "DISCONNECTED"
        )


class HonConfigSelectEntity(HonSelectEntity):
    entity_description: HonConfigSelectEntityDescription

    async def async_select_option(self, option: str) -> None:
        self._device.settings[self.entity_description.key].value = option
        await self.coordinator.async_refresh()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return super(SelectEntity, self).available
