import logging

import pkg_resources
from homeassistant.components import persistent_notification
from homeassistant.components.button import ButtonEntityDescription, ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity import EntityCategory
from pyhon.appliance import HonAppliance

from .const import DOMAIN
from .hon import HonEntity

_LOGGER = logging.getLogger(__name__)

BUTTONS: dict[str, tuple[ButtonEntityDescription, ...]] = {
    "IH": (
        ButtonEntityDescription(
            key="startProgram",
            name="Start Program",
            icon="mdi:pot-steam",
            translation_key="induction_hob",
        ),
    ),
    "REF": (
        ButtonEntityDescription(
            key="startProgram",
            name="Program Start",
            icon="mdi:play",
            translation_key="start_program",
        ),
        ButtonEntityDescription(
            key="stopProgram",
            name="Program Stop",
            icon="mdi:stop",
            translation_key="stop_program",
        ),
    ),
    "HO": (
        ButtonEntityDescription(
            key="startProgram",
            name="Start Program",
            icon="mdi:hvac",
            translation_key="start_program",
        ),
        ButtonEntityDescription(
            key="stopProgram",
            name="Stop Program",
            icon="mdi:hvac-off",
            translation_key="stop_program",
        ),
    ),
}


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities) -> None:
    entities = []
    for device in hass.data[DOMAIN][entry.unique_id].appliances:
        for description in BUTTONS.get(device.appliance_type, []):
            if not device.commands.get(description.key):
                continue
            entity = HonButtonEntity(hass, entry, device, description)
            await entity.coordinator.async_config_entry_first_refresh()
            entities.append(entity)
        entities.append(HonFeatureRequestButton(hass, entry, device))
        await entities[-1].coordinator.async_config_entry_first_refresh()
    async_add_entities(entities)


class HonButtonEntity(HonEntity, ButtonEntity):
    entity_description: ButtonEntityDescription

    async def async_press(self) -> None:
        await self._device.commands[self.entity_description.key].send()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            and int(self._device.get("remoteCtrValid", "1")) == 1
            and self._device.get("attributes.lastConnEvent.category") != "DISCONNECTED"
        )


class HonFeatureRequestButton(HonEntity, ButtonEntity):
    def __init__(self, hass, entry, device: HonAppliance) -> None:
        super().__init__(hass, entry, device)

        self._attr_unique_id = f"{super().unique_id}_log_device_info"
        self._attr_icon = "mdi:information"
        self._attr_name = "Show Device Info"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_entity_registry_enabled_default = False

    async def async_press(self) -> None:
        pyhon_version = pkg_resources.get_distribution("pyhon").version
        info = f"{self._device.diagnose()}pyhOnVersion: {pyhon_version}"
        title = f"{self._device.nick_name} Device Info"
        persistent_notification.create(
            self._hass, f"````\n```\n{info}\n```\n````", title
        )
        _LOGGER.info(info.replace(" ", "\u200B "))
