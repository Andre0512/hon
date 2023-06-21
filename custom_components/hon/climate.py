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
    TEMP_CELSIUS,
)
from homeassistant.core import callback
from pyhon.appliance import HonAppliance

from .const import HON_HVAC_MODE, HON_FAN, DOMAIN
from .hon import HonEntity

_LOGGER = logging.getLogger(__name__)


@dataclass
class HonACClimateEntityDescription(ClimateEntityDescription):
    pass


@dataclass
class HonClimateEntityDescription(ClimateEntityDescription):
    mode: HVACMode = "auto"


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
        HonClimateEntityDescription(
            key="settings.tempSelZ1",
            mode=HVACMode.COOL,
            name="Fridge",
            icon="mdi:thermometer",
            translation_key="fridge",
        ),
        HonClimateEntityDescription(
            key="settings.tempSelZ2",
            mode=HVACMode.COOL,
            name="Freezer",
            icon="mdi:snowflake-thermometer",
            translation_key="freezer",
        ),
    ),
    "OV": (
        HonClimateEntityDescription(
            key="settings.tempSel",
            mode=HVACMode.HEAT,
            name="Oven",
            icon="mdi:thermometer",
            translation_key="oven",
        ),
    ),
    "WC": (
        HonClimateEntityDescription(
            key="settings.tempSel",
            mode=HVACMode.COOL,
            name="Wine Cellar",
            icon="mdi:thermometer",
            translation_key="wine",
        ),
        HonClimateEntityDescription(
            key="settings.tempSelZ2",
            mode=HVACMode.COOL,
            name="Wine Cellar",
            icon="mdi:thermometer",
            translation_key="wine",
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
            elif isinstance(description, HonClimateEntityDescription):
                if description.key not in device.available_settings:
                    continue
                entity = HonClimateEntity(hass, entry, device, description)
            else:
                continue
            await entity.coordinator.async_config_entry_first_refresh()
            entities.append(entity)
    async_add_entities(entities)


class HonACClimateEntity(HonEntity, ClimateEntity):
    def __init__(self, hass, entry, device: HonAppliance, description) -> None:
        super().__init__(hass, entry, device, description)

        self._attr_temperature_unit = TEMP_CELSIUS
        self._set_temperature_bound()

        self._attr_hvac_modes = [HVACMode.OFF]
        for mode in device.settings["settings.machMode"].values:
            self._attr_hvac_modes.append(HON_HVAC_MODE[mode])
        self._attr_preset_modes = []
        for mode in device.settings["startProgram.program"].values:
            self._attr_preset_modes.append(mode)
        self._attr_fan_modes = [FAN_OFF]
        for mode in device.settings["settings.windSpeed"].values:
            self._attr_fan_modes.append(HON_FAN[mode])
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
            | ClimateEntityFeature.PRESET_MODE
        )

        self._handle_coordinator_update(update=False)

    def _set_temperature_bound(self) -> None:
        self._attr_target_temperature_step = self._device.settings[
            "settings.tempSel"
        ].step
        self._attr_max_temp = self._device.settings["settings.tempSel"].max
        self._attr_min_temp = self._device.settings["settings.tempSel"].min

    @property
    def target_temperature(self) -> int | None:
        """Return the temperature we try to reach."""
        return int(float(self._device.get("tempSel")))

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        return float(self._device.get("tempIndoor"))

    async def async_set_temperature(self, **kwargs):
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is None:
            return False
        self._device.settings["settings.tempSel"].value = str(int(temperature))
        await self._device.commands["settings"].send()
        self.async_write_ha_state()

    @property
    def hvac_mode(self) -> HVACMode | str | None:
        if self._device.get("onOffStatus") == "0":
            return HVACMode.OFF
        else:
            return HON_HVAC_MODE[self._device.get("machMode")]

    async def async_set_hvac_mode(self, hvac_mode):
        self._attr_hvac_mode = hvac_mode
        if hvac_mode == HVACMode.OFF:
            await self._device.commands["stopProgram"].send()
            self._device.sync_command("stopProgram", "settings")
        else:
            self._device.settings["settings.onOffStatus"].value = "1"
            setting = self._device.settings["settings.machMode"]
            modes = {HON_HVAC_MODE[number]: number for number in setting.values}
            setting.value = modes[hvac_mode]
            await self._device.commands["settings"].send()
        self.async_write_ha_state()

    @property
    def preset_mode(self) -> str | None:
        """Return the current Preset for this channel."""
        return None

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set the new preset mode."""
        if program := self._device.settings.get(f"startProgram.program"):
            program.value = preset_mode
        self._device.sync_command("startProgram", "settings")
        self._set_temperature_bound()
        self._handle_coordinator_update(update=False)
        await self.coordinator.async_refresh()
        self._attr_preset_mode = preset_mode
        await self._device.commands["startProgram"].send()
        self.async_write_ha_state()

    @property
    def fan_mode(self) -> str | None:
        """Return the fan setting."""
        return HON_FAN[self._device.get("windSpeed")]

    async def async_set_fan_mode(self, fan_mode):
        mode_number = list(HON_FAN.values()).index(fan_mode)
        mode = list(HON_FAN.keys())[mode_number]
        self._device.settings["settings.windSpeed"].value = mode
        self._attr_fan_mode = fan_mode
        await self._device.commands["settings"].send()
        self.async_write_ha_state()

    @property
    def swing_mode(self) -> str | None:
        """Return the swing setting."""
        horizontal = self._device.get("windDirectionHorizontal")
        vertical = self._device.get("windDirectionVertical")
        if horizontal == "7" and vertical == "8":
            return SWING_BOTH
        elif horizontal == "7":
            return SWING_HORIZONTAL
        elif vertical == "8":
            return SWING_VERTICAL
        else:
            return SWING_OFF

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

    @callback
    def _handle_coordinator_update(self, update=True) -> None:
        self._attr_target_temperature = self.target_temperature
        self._attr_current_temperature = self.current_temperature
        self._attr_hvac_mode = self.hvac_mode
        self._attr_fan_mode = self.fan_mode
        self._attr_swing_mode = self.swing_mode
        if update:
            self.async_write_ha_state()


class HonClimateEntity(HonEntity, ClimateEntity):
    entity_description: HonClimateEntityDescription

    def __init__(self, hass, entry, device: HonAppliance, description) -> None:
        super().__init__(hass, entry, device, description)

        self._attr_temperature_unit = TEMP_CELSIUS
        self._set_temperature_bound()

        self._attr_supported_features = (
            ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.PRESET_MODE
        )

        self._attr_hvac_modes = [description.mode]
        if "stopProgram" in device.commands:
            self._attr_hvac_modes += [HVACMode.OFF]
            modes = []
        else:
            modes = ["no_mode"]

        for mode, data in device.commands["startProgram"].categories.items():
            if mode not in data.parameters["program"].values:
                continue
            if zone := data.parameters.get("zone"):
                if self.entity_description.name.lower() in zone.values:
                    modes.append(mode)
            else:
                modes.append(mode)
        self._attr_preset_modes = modes

        self._handle_coordinator_update(update=False)

    @property
    def target_temperature(self) -> float | None:
        """Return the temperature we try to reach."""
        return float(self._device.get(self.entity_description.key))

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        temp_key = self.entity_description.key.split(".")[-1].replace("Sel", "")
        return float(self._device.get(temp_key))

    async def async_set_temperature(self, **kwargs):
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is None:
            return False
        self._device.settings[self.entity_description.key].value = str(int(temperature))
        await self._device.commands["settings"].send()
        self.async_write_ha_state()

    @property
    def hvac_mode(self) -> HVACMode | str | None:
        if self._device.get("onOffStatus") == "0":
            return HVACMode.OFF
        else:
            return self.entity_description.mode

    async def async_set_hvac_mode(self, hvac_mode):
        if len(self.hvac_modes) <= 1:
            return
        if hvac_mode == HVACMode.OFF:
            await self._device.commands["stopProgram"].send()
        else:
            await self._device.commands["startProgram"].send()
        self._attr_hvac_mode = hvac_mode
        self.async_write_ha_state()

    @property
    def preset_mode(self) -> str | None:
        """Return the current Preset for this channel."""
        if self._device.get("onOffStatus") is not None:
            return self._device.get("programName", "")
        else:
            return self._device.get(
                f"mode{self.entity_description.key[-2:]}", "no_mode"
            )

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set the new preset mode."""
        command = "stopProgram" if preset_mode == "no_mode" else "startProgram"
        if program := self._device.settings.get(f"{command}.program"):
            program.value = preset_mode
        if zone := self._device.settings.get(f"{command}.zone"):
            zone.value = self.entity_description.name.lower()
        self._device.sync_command(command, "settings")
        self._set_temperature_bound()
        await self.coordinator.async_refresh()
        await self._device.commands[command].send()
        self._attr_preset_mode = preset_mode
        self.async_write_ha_state()

    def _set_temperature_bound(self):
        self._attr_target_temperature_step = self._device.settings[
            self.entity_description.key
        ].step
        self._attr_max_temp = self._device.settings[self.entity_description.key].max
        self._attr_min_temp = self._device.settings[self.entity_description.key].min

    @callback
    def _handle_coordinator_update(self, update=True) -> None:
        self._attr_target_temperature = self.target_temperature
        self._attr_current_temperature = self.current_temperature
        self._attr_hvac_mode = self.hvac_mode
        self._attr_preset_mode = self.preset_mode
        if update:
            self.async_write_ha_state()
