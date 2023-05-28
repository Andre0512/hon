import logging
from dataclasses import dataclass

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityDescription,
)
from homeassistant.components.climate.const import (
    FAN_OFF,
    SWING_OFF,
    SWING_BOTH,
    SWING_VERTICAL,
    SWING_HORIZONTAL,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_TEMPERATURE,
    PRECISION_WHOLE,
    TEMP_CELSIUS,
)
from homeassistant.core import callback
from pyhon import helper
from pyhon.appliance import HonAppliance

from .const import HON_HVAC_MODE, HON_FAN, HON_HVAC_PROGRAM, DOMAIN
from .hon import HonEntity

_LOGGER = logging.getLogger(__name__)


@dataclass
class HonACClimateEntityDescription(ClimateEntityDescription):
    pass


@dataclass
class HonREFClimateEntityDescription(ClimateEntityDescription):
    pass


CLIMATES = {
    "AC": (
        HonACClimateEntityDescription(
            key="settings",
            name="Air Conditioner",
            icon="mdi:air-conditioner",
            translation_key="air_conditioner",
        ),
    ),
    "REF": (
        HonREFClimateEntityDescription(
            key="settings.tempSelZ1",
            name="Fridge",
            icon="mdi:thermometer",
            translation_key="fridge",
        ),
        HonREFClimateEntityDescription(
            key="settings.tempSelZ2",
            name="Freezer",
            icon="mdi:snowflake-thermometer",
            translation_key="freezer",
        ),
    ),
}


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities) -> None:
    entities = []
    for device in hass.data[DOMAIN][entry.unique_id].appliances:
        for description in CLIMATES.get(device.appliance_type, []):
            if isinstance(description, HonACClimateEntityDescription):
                if description.key not in list(device.commands):
                    continue
                entity = HonACClimateEntity(hass, entry, device, description)
            elif isinstance(description, HonREFClimateEntityDescription):
                if description.key not in device.available_settings:
                    continue
                entity = HonREFClimateEntity(hass, entry, device, description)
            else:
                continue
            await entity.coordinator.async_config_entry_first_refresh()
            entities.append(entity)
    async_add_entities(entities)


class HonACClimateEntity(HonEntity, ClimateEntity):
    def __init__(self, hass, entry, device: HonAppliance, description) -> None:
        super().__init__(hass, entry, device, description)

        self._attr_temperature_unit = TEMP_CELSIUS
        self._attr_target_temperature_step = PRECISION_WHOLE
        self._attr_max_temp = device.settings["settings.tempSel"].max
        self._attr_min_temp = device.settings["settings.tempSel"].min

        self._attr_hvac_modes = [HVACMode.OFF] + [
            HON_HVAC_MODE[mode] for mode in device.settings["settings.machMode"].values
        ]
        self._attr_fan_modes = [FAN_OFF] + [
            HON_FAN[mode] for mode in device.settings["settings.windSpeed"].values
        ]
        self._attr_swing_modes = [
            SWING_OFF,
            SWING_VERTICAL,
            SWING_HORIZONTAL,
            SWING_BOTH,
        ]
        self._attr_supported_features = (
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.FAN_MODE
            | ClimateEntityFeature.SWING_MODE
        )

        self._handle_coordinator_update(update=False)

    async def async_set_hvac_mode(self, hvac_mode):
        if self._device.get("onOffStatus") == "0":
            self._attr_hvac_mode = HVACMode.OFF
        else:
            self._attr_hvac_mode = HON_HVAC_MODE[self._device.get("machMode")]
        if hvac_mode == HVACMode.OFF:
            await self._device.commands["stopProgram"].send()
        else:
            self._device.settings["startProgram.program"].value = HON_HVAC_PROGRAM[
                hvac_mode
            ]
            await self._device.commands["startProgram"].send()
        self._attr_hvac_mode = hvac_mode
        self.async_write_ha_state()

    async def async_set_fan_mode(self, fan_mode):
        mode_number = list(HON_FAN.values()).index(fan_mode)
        self._device.settings["settings.windSpeed"].value = list(HON_FAN.keys())[
            mode_number
        ]
        await self._device.commands["settings"].send()
        self.async_write_ha_state()

    async def async_set_swing_mode(self, swing_mode):
        horizontal = self._device.settings["settings.windDirectionHorizontal"]
        vertical = self._device.settings["settings.windDirectionVertical"]
        if swing_mode in [SWING_BOTH, SWING_HORIZONTAL]:
            horizontal.value = "7"
        if swing_mode in [SWING_BOTH, SWING_VERTICAL]:
            vertical.value = "8"
        if swing_mode in [SWING_OFF, SWING_HORIZONTAL] and vertical.value == "8":
            vertical.value = "5"
        if swing_mode in [SWING_OFF, SWING_VERTICAL] and horizontal.value == "7":
            horizontal.value = "0"
        self._attr_swing_mode = swing_mode
        await self._device.commands["settings"].send()
        self.async_write_ha_state()

    async def async_set_temperature(self, **kwargs):
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is None:
            return False
        self._device.settings["settings.tempSel"].value = str(int(temperature))
        await self._device.commands["settings"].send()
        self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self, update=True) -> None:
        self._attr_target_temperature = int(float(self._device.get("tempSel")))
        self._attr_current_temperature = float(self._device.get("tempIndoor"))

        if self._device.get("onOffStatus") == "0":
            self._attr_hvac_mode = HVACMode.OFF
        else:
            self._attr_hvac_mode = HON_HVAC_MODE[self._device.get("machMode")]

        self._attr_fan_mode = HON_FAN[self._device.get("windSpeed")]

        horizontal = self._device.get("windDirectionHorizontal")
        vertical = self._device.get("windDirectionVertical")
        if horizontal == "7" and vertical == "8":
            self._attr_swing_mode = SWING_BOTH
        elif horizontal == "7":
            self._attr_swing_mode = SWING_HORIZONTAL
        elif vertical == "8":
            self._attr_swing_mode = SWING_VERTICAL
        else:
            self._attr_swing_mode = SWING_OFF
        if update:
            self.async_write_ha_state()


class HonREFClimateEntity(HonEntity, ClimateEntity):
    def __init__(self, hass, entry, device: HonAppliance, description) -> None:
        super().__init__(hass, entry, device, description)

        self._attr_temperature_unit = TEMP_CELSIUS
        self._attr_target_temperature_step = PRECISION_WHOLE
        self._attr_max_temp = device.settings[description.key].max
        self._attr_min_temp = device.settings[description.key].min

        self._attr_hvac_modes = [HVACMode.COOL]
        self._attr_supported_features = (
            ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.PRESET_MODE
        )

        self._handle_coordinator_update(update=False)

        modes = ["no_mode"]
        for mode, data in device.commands["startProgram"].categories.items():
            if zone := data.parameters.get("zone"):
                if self.entity_description.name.lower() in zone.values:
                    modes.append(mode)
        self._attr_preset_modes = modes

    @property
    def target_temperature(self) -> int | None:
        """Return the temperature we try to reach."""
        return int(self._device.get(self.entity_description.key))

    @property
    def current_temperature(self) -> int | None:
        """Return the current temperature."""
        temp_key = self.entity_description.key.split(".")[-1].replace("Sel", "")
        return int(self._device.get(temp_key))

    async def async_set_temperature(self, **kwargs):
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is None:
            return False
        self._device.settings[self.entity_description.key].value = str(int(temperature))
        await self._device.commands["settings"].send()
        self.async_write_ha_state()

    @property
    def preset_mode(self) -> str | None:
        """Return the current Preset for this channel."""
        return self._device.get(f"mode{self.entity_description.key[-2:]}", "no_mode")

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set the new preset mode."""
        if preset_mode == "no_mode":
            self._device.sync_command("stopProgram", "settings")
            await self.coordinator.async_refresh()
            await self._device.commands["stopProgram"].send()
        else:
            self._device.settings["startProgram.program"].value = preset_mode
            self._device.settings[
                "startProgram.zone"
            ].value = self.entity_description.name.lower()
            self._device.sync_command("startProgram", "settings")
            await self.coordinator.async_refresh()
            await self._device.commands["startProgram"].send()
        self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self, update=True) -> None:
        self._attr_target_temperature = int(
            float(self._device.get(self.entity_description.key))
        )
        temp_key = self.entity_description.key.split(".")[-1].replace("Sel", "")
        self._attr_current_temperature = int(self._device.get(temp_key))

        self._attr_hvac_mode = HVACMode.COOL
        if update:
            self.async_write_ha_state()
