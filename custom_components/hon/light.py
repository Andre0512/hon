import logging
from typing import Any

from homeassistant.components.light import (
    LightEntityDescription,
    LightEntity,
    ColorMode,
    ATTR_BRIGHTNESS,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from pyhon.appliance import HonAppliance
from pyhon.parameter.range import HonParameterRange

from .const import DOMAIN
from .hon import HonEntity

_LOGGER = logging.getLogger(__name__)


LIGHTS = {
    "WC": (
        LightEntityDescription(
            key="settings.lightStatus",
            name="Light",
            translation_key="light",
        ),
    ),
    "HO": (
        LightEntityDescription(
            key="settings.lightStatus",
            name="Light status",
            translation_key="light",
        ),
    ),
    "AP": (
        LightEntityDescription(
            key="settings.lightStatus",
            name="Light status",
            translation_key="light",
        ),
    ),
}


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities) -> None:
    entities = []
    for device in hass.data[DOMAIN][entry.unique_id].appliances:
        for description in LIGHTS.get(device.appliance_type, []):
            if (
                description.key not in device.available_settings
                or device.get(description.key.split(".")[-1]) is None
            ):
                continue
            entity = HonLightEntity(hass, entry, device, description)
            await entity.coordinator.async_config_entry_first_refresh()
            entities.append(entity)
    async_add_entities(entities)


class HonLightEntity(HonEntity, LightEntity):
    entity_description: LightEntityDescription

    def __init__(self, hass, entry, device: HonAppliance, description) -> None:
        light: HonParameterRange = device.settings.get(description.key)
        self._light_range = (light.min, light.max)
        self._attr_supported_color_modes: set[ColorMode] = set()
        if len(light.values) == 2:
            self._attr_supported_color_modes.add(ColorMode.ONOFF)
        else:
            self._attr_supported_color_modes.add(ColorMode.BRIGHTNESS)
        self._command, self._parameter = description.key.split(".")
        super().__init__(hass, entry, device, description)
        self._handle_coordinator_update(update=False)

    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        return self._device.get(self.entity_description.key.split(".")[-1]) > 0

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on or control the light."""
        light: HonParameterRange = self._device.settings.get(
            self.entity_description.key
        )
        if ColorMode.BRIGHTNESS in self._attr_supported_color_modes:
            percent = int(100 / 255 * kwargs.get(ATTR_BRIGHTNESS, 128))
            light.value = round(light.max / 100 * percent)
            if light.value == light.min:
                self._attr_is_on = False
            self._attr_brightness = self.brightness
        else:
            light.value = light.max
        await self._device.commands[self._command].send()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Instruct the light to turn off."""
        light: HonParameterRange = self._device.settings.get(
            self.entity_description.key
        )
        light.value = light.min
        await self._device.commands[self._command].send()
        self.async_write_ha_state()

    @property
    def brightness(self) -> int | None:
        """Return the brightness of the light."""
        light: HonParameterRange = self._device.settings.get(
            self.entity_description.key
        )
        if light.value == light.min:
            return None
        return int(255 / light.max * light.value)

    @callback
    def _handle_coordinator_update(self, update=True) -> None:
        self._attr_is_on = self.is_on
        self._attr_brightness = self.brightness
        if update:
            self.async_write_ha_state()

    @property
    def available(self) -> bool:
        return (
            super().available
            and len(self._device.settings.get(self.entity_description.key).values) > 1
        )
