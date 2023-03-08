from dataclasses import dataclass
from typing import Any

from homeassistant.components.switch import SwitchEntityDescription, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from pyhon import HonConnection
from pyhon.device import HonDevice

from .const import DOMAIN
from .hon import HonCoordinator, HonEntity


@dataclass
class HonSwitchEntityDescriptionMixin:
    turn_on_key: str = ""
    turn_off_key: str = ""


@dataclass
class HonSwitchEntityDescription(HonSwitchEntityDescriptionMixin,
    SwitchEntityDescription
):
    pass


SWITCHES: dict[str, tuple[HonSwitchEntityDescription, ...]] = {
    "WM": (
        HonSwitchEntityDescription(
            key="active",
            name="Washing Machine",
            icon="mdi:washing-machine",
            turn_on_key="startProgram",
            turn_off_key="stopProgram",
        ),
        HonSwitchEntityDescription(
            key="pause",
            name="Pause Washing Machine",
            icon="mdi:pause",
            turn_on_key="pauseProgram",
            turn_off_key="resumeProgram",
        ),
        HonSwitchEntityDescription(
            key="startProgram.delayStatus",
            name="Delay Status",
            icon="mdi:timer-check",
            entity_category=EntityCategory.CONFIG
        ),
        HonSwitchEntityDescription(
            key="startProgram.haier_SoakPrewashSelection",
            name="Soak Prewash Selection",
            icon="mdi:tshirt-crew",
            entity_category=EntityCategory.CONFIG
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

        if descriptions := SWITCHES.get(device.appliance_type):
            for description in descriptions:
                if device.get(description.key) is not None or device.commands.get(description.key) is not None:
                    appliances.extend([
                        HonSwitchEntity(hass, coordinator, entry, device, description)]
                    )

    async_add_entities(appliances)


class HonSwitchEntity(HonEntity, SwitchEntity):
    entity_description: HonSwitchEntityDescription

    def __init__(self, hass, coordinator, entry, device: HonDevice, description: HonSwitchEntityDescription) -> None:
        super().__init__(hass, entry, coordinator, device)
        self._coordinator = coordinator
        self._device = device
        self.entity_description = description
        self._attr_unique_id = f"{super().unique_id}{description.key}"

    def available(self) -> bool:
        if self.entity_category == EntityCategory.CONFIG:
            return self._device.settings[self.entity_description.key].typology != "fixed"
        return True

    @property
    def is_on(self) -> bool | None:
        """Return True if entity is on."""
        if self.entity_category == EntityCategory.CONFIG:
            setting = self._device.settings[self.entity_description.key]
            return setting.value == "1" or hasattr(setting, "min") and setting.value != setting.min
        return self._device.get(self.entity_description.key, False)

    async def async_turn_on(self, **kwargs: Any) -> None:
        if self.entity_category == EntityCategory.CONFIG:
            setting = self._device.settings[self.entity_description.key]
            setting.value = setting.max
            self.async_write_ha_state()
        else:
            await self._device.commands[self.entity_description.turn_on_key].send()

    async def async_turn_off(self, **kwargs: Any) -> None:
        if self.entity_category == EntityCategory.CONFIG:
            setting = self._device.settings[self.entity_description.key]
            setting.value = setting.min
            self.async_write_ha_state()
        else:
            await self._device.commands[self.entity_description.turn_off_key].send()


