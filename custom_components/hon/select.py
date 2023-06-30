from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, List

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature, UnitOfTime, REVOLUTIONS_PER_MINUTE
from homeassistant.core import callback
from homeassistant.helpers.entity import EntityCategory

from . import const
from .const import DOMAIN
from .hon import HonEntity, unique_entities, get_readable

_LOGGER = logging.getLogger(__name__)


@dataclass
class HonSelectEntityDescription(SelectEntityDescription):
    option_list: Dict[int, str] = None


@dataclass
class HonConfigSelectEntityDescription(SelectEntityDescription):
    entity_category: EntityCategory = EntityCategory.CONFIG
    option_list: Dict[int, str] = None


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
            option_list=const.TUMBLE_DRYER_DRY_LEVEL,
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
            option_list=const.AC_HUMAN_SENSE,
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
    "AP": (
        HonSelectEntityDescription(
            key="settings.aromaStatus",
            name="Diffuser Level",
            option_list=const.AP_DIFFUSER_LEVEL,
            translation_key="diffuser",
        ),
        HonSelectEntityDescription(
            key="settings.machMode",
            name="Mode",
            icon="mdi:run",
            option_list=const.AP_MACH_MODE,
            translation_key="mode",
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


class HonConfigSelectEntity(HonEntity, SelectEntity):
    entity_description: HonConfigSelectEntityDescription

    @property
    def current_option(self) -> str | None:
        if not (setting := self._device.settings.get(self.entity_description.key)):
            return None
        value = get_readable(self.entity_description, setting.value)
        if value not in self._attr_options:
            return None
        return value

    @property
    def options(self) -> list[str]:
        setting = self._device.settings.get(self.entity_description.key)
        if setting is None:
            return []
        return [get_readable(self.entity_description, key) for key in setting.values]

    def _option_to_number(self, option: str, values: List[str]):
        if (options := self.entity_description.option_list) is not None:
            return next(
                (k for k, v in options.items() if str(k) in values and v == option),
                option,
            )
        return option

    async def async_select_option(self, option: str) -> None:
        setting = self._device.settings[self.entity_description.key]
        setting.value = self._option_to_number(option, setting.values)
        await self.coordinator.async_refresh()

    @callback
    def _handle_coordinator_update(self, update=True) -> None:
        self._attr_available = self.available
        self._attr_options = self.options
        self._attr_current_option = self.current_option
        if update:
            self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._device.settings.get(self.entity_description.key) is not None


class HonSelectEntity(HonConfigSelectEntity):
    entity_description: HonSelectEntityDescription

    async def async_select_option(self, option: str) -> None:
        setting = self._device.settings[self.entity_description.key]
        setting.value = self._option_to_number(option, setting.values)
        command = self.entity_description.key.split(".")[0]
        await self._device.commands[command].send()
        if command != "settings":
            self._device.sync_command(command, "settings")
        await self.coordinator.async_refresh()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            and int(self._device.get("remoteCtrValid", 1)) == 1
            and self._device.get("attributes.lastConnEvent.category") != "DISCONNECTED"
        )
