import logging

import pkg_resources

from homeassistant.components import persistent_notification
from homeassistant.components.button import ButtonEntityDescription, ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from pyhon import Hon
from pyhon.appliance import HonAppliance

from .const import DOMAIN
from .hon import HonCoordinator, HonEntity

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
}


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

        if descriptions := BUTTONS.get(device.appliance_type):
            for description in descriptions:
                if not device.commands.get(description.key):
                    continue
                appliances.extend(
                    [HonButtonEntity(hass, coordinator, entry, device, description)]
                )
        appliances.extend([HonFeatureRequestButton(hass, coordinator, entry, device)])

    async_add_entities(appliances)


class HonButtonEntity(HonEntity, ButtonEntity):
    def __init__(
        self, hass, coordinator, entry, device: HonAppliance, description
    ) -> None:
        super().__init__(hass, entry, coordinator, device)

        self._coordinator = coordinator
        self._device = device
        self.entity_description = description
        self._attr_unique_id = f"{super().unique_id}{description.key}"

    async def async_press(self) -> None:
        await self._device.commands[self.entity_description.key].send()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            and self._device.get("remoteCtrValid", "1") == "1"
            and self._device.get("attributes.lastConnEvent.category") != "DISCONNECTED"
        )


class HonFeatureRequestButton(HonEntity, ButtonEntity):
    def __init__(self, hass, coordinator, entry, device: HonAppliance) -> None:
        super().__init__(hass, entry, coordinator, device)
        self._hass = hass

        self._device = device
        self._attr_unique_id = f"{super().unique_id}_log_device_info"
        self._attr_icon = "mdi:information"
        self._attr_name = "Show Device Info"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        self._attr_entity_registry_enabled_default = False

    async def async_press(self) -> None:
        pyhon_version = pkg_resources.get_distribution("pyhon").version
        info = f"Device Info:\n{self._device.diagnose()}pyhOnVersion: {pyhon_version}"
        title = f"{self._device.nick_name} Device Info"
        persistent_notification.create(self._hass, f"```\n```{info}```\n```", title)
        _LOGGER.info(info.replace(" ", "\u200B "))
