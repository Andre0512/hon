import logging
from dataclasses import dataclass

from pyhon import Hon

from homeassistant.components.binary_sensor import (
    BinarySensorEntityDescription,
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from .const import DOMAIN
from .hon import HonCoordinator, HonEntity

_LOGGER = logging.getLogger(__name__)


@dataclass
class HonBinarySensorEntityDescriptionMixin:
    on_value: str = ""


@dataclass
class HonBinarySensorEntityDescription(
    HonBinarySensorEntityDescriptionMixin, BinarySensorEntityDescription
):
    pass


BINARY_SENSORS: dict[str, tuple[HonBinarySensorEntityDescription, ...]] = {
    "WM": (
        HonBinarySensorEntityDescription(
            key="attributes.lastConnEvent.category",
            name="Remote Control",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            on_value="CONNECTED",
            icon="mdi:remote",
        ),
        HonBinarySensorEntityDescription(
            key="doorLockStatus",
            name="Door Lock",
            device_class=BinarySensorDeviceClass.LOCK,
            on_value="0",
        ),
        HonBinarySensorEntityDescription(
            key="doorStatus",
            name="Door",
            device_class=BinarySensorDeviceClass.DOOR,
            on_value="1",
        ),
    ),
    "TD": (
        HonBinarySensorEntityDescription(
            key="attributes.lastConnEvent.category",
            name="Connection",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            on_value="CONNECTED",
        ),
        HonBinarySensorEntityDescription(
            key="doorStatus",
            name="Door",
            device_class=BinarySensorDeviceClass.DOOR,
            on_value="1",
        ),
    ),
    "WD": (
        HonBinarySensorEntityDescription(
            key="attributes.lastConnEvent.category",
            name="Remote Control",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            on_value="CONNECTED",
            icon="mdi:remote",
        ),
        HonBinarySensorEntityDescription(
            key="startProgram.prewash",
            name="Pre Wash",
        ),
        HonBinarySensorEntityDescription(
            key="extraRinse1",
            name="Extra Rinse 1",
        ),
        HonBinarySensorEntityDescription(
            key="extraRinse2",
            name="Extra Rinse 2",
        ),
        HonBinarySensorEntityDescription(
            key="extraRinse3",
            name="Extra Rinse 3",
        ),
        HonBinarySensorEntityDescription(
            key="goodNight",
            name="Good Night Mode",
        ),
        HonBinarySensorEntityDescription(
            key="acquaplus",
            name="Acqua Plus",
        ),
        HonBinarySensorEntityDescription(
            key="anticrease",
            name="Anti-Crease",
        ),
    ),
    "OV": (
        HonBinarySensorEntityDescription(
            key="attributes.lastConnEvent.category",
            name="Connection",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            on_value="CONNECTED",
            icon="mdi:wifi",
        ),
        HonBinarySensorEntityDescription(
            key="attributes.parameters.remoteCtrValid",
            name="Remote Control",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            on_value="1",
            icon="mdi:remote",
        ),
        HonBinarySensorEntityDescription(
            key="attributes.parameters.onOffStatus",
            name="On",
            device_class=BinarySensorDeviceClass.RUNNING,
            on_value="1",
            icon="mdi:power-cycle",
        ),
    ),
    "IH": (
        HonBinarySensorEntityDescription(
            key="attributes.lastConnEvent.category",
            name="Connection",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            on_value="CONNECTED",
            icon="mdi:wifi",
        ),
        HonBinarySensorEntityDescription(
            key="attributes.parameters.remoteCtrValid",
            name="Remote Control",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            on_value="1",
            icon="mdi:remote",
        ),
        HonBinarySensorEntityDescription(
            key="attributes.parameters.onOffStatus",
            name="On",
            device_class=BinarySensorDeviceClass.RUNNING,
            on_value="1",
            icon="mdi:power-cycle",
        ),
        HonBinarySensorEntityDescription(
            key="hotStatus",
            name="Hot Status",
            device_class=BinarySensorDeviceClass.HEAT,
            on_value="1",
        ),
        HonBinarySensorEntityDescription(
            key="hobLockStatus",
            name="Hob Lock",
            device_class=BinarySensorDeviceClass.LOCK,
            on_value="0",
        ),
    ),
    "DW": (
        HonBinarySensorEntityDescription(
            key="saltStatus",
            name="Salt",
            device_class=BinarySensorDeviceClass.PROBLEM,
            on_value="1",
            icon="mdi:shaker-outline",
        ),
        HonBinarySensorEntityDescription(
            key="rinseAidStatus",
            name="Rinse Aid",
            device_class=BinarySensorDeviceClass.PROBLEM,
            on_value="1",
            icon="mdi:spray-bottle",
        ),
        HonBinarySensorEntityDescription(
            key="attributes.lastConnEvent.category",
            name="Connection",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            on_value="CONNECTED",
        ),
        HonBinarySensorEntityDescription(
            key="doorStatus",
            name="Door",
            device_class=BinarySensorDeviceClass.DOOR,
            on_value="1",
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

        if descriptions := BINARY_SENSORS.get(device.appliance_type):
            for description in descriptions:
                if not device.get(description.key):
                    _LOGGER.warning(
                        "[%s] Can't setup %s", device.appliance_type, description.key
                    )
                    continue
                appliances.extend(
                    [
                        HonBinarySensorEntity(
                            hass, coordinator, entry, device, description
                        )
                    ]
                )

    async_add_entities(appliances)


class HonBinarySensorEntity(HonEntity, BinarySensorEntity):
    entity_description: HonBinarySensorEntityDescription

    def __init__(self, hass, coordinator, entry, device, description) -> None:
        super().__init__(hass, entry, coordinator, device)

        self._coordinator = coordinator

        self.entity_description = description
        self._attr_unique_id = f"{super().unique_id}{description.key}"

    @property
    def is_on(self) -> bool:
        return (
            self._device.get(self.entity_description.key, "")
            == self.entity_description.on_value
        )

    @callback
    def _handle_coordinator_update(self):
        self._attr_native_value = (
            self._device.get(self.entity_description.key, "")
            == self.entity_description.on_value
        )
        self.async_write_ha_state()
