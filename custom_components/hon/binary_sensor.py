import logging
from dataclasses import dataclass

from homeassistant.components.binary_sensor import (
    BinarySensorEntityDescription,
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback

from .const import DOMAIN
from .hon import HonEntity, unique_entities

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
            translation_key="remote_control",
        ),
        HonBinarySensorEntityDescription(
            key="doorLockStatus",
            name="Door Lock",
            device_class=BinarySensorDeviceClass.LOCK,
            on_value="0",
            translation_key="door_lock",
        ),
        HonBinarySensorEntityDescription(
            key="doorStatus",
            name="Door",
            device_class=BinarySensorDeviceClass.DOOR,
            on_value="1",
            translation_key="door_open",
        ),
        HonBinarySensorEntityDescription(
            key="startProgram.prewash", name="Pre Wash", translation_key="prewash"
        ),
        HonBinarySensorEntityDescription(
            key="extraRinse1", name="Extra Rinse 1", translation_key="extra_rinse_1"
        ),
        HonBinarySensorEntityDescription(
            key="extraRinse2", name="Extra Rinse 2", translation_key="extra_rinse_2"
        ),
        HonBinarySensorEntityDescription(
            key="extraRinse3", name="Extra Rinse 3", translation_key="extra_rinse_3"
        ),
        HonBinarySensorEntityDescription(
            key="goodNight", name="Good Night Mode", translation_key="good_night"
        ),
        HonBinarySensorEntityDescription(
            key="acquaplus", name="Acqua Plus", translation_key="acqua_plus"
        ),
    ),
    "TD": (
        HonBinarySensorEntityDescription(
            key="attributes.lastConnEvent.category",
            name="Connection",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            on_value="CONNECTED",
            translation_key="connection",
        ),
        HonBinarySensorEntityDescription(
            key="doorStatus",
            name="Door",
            device_class=BinarySensorDeviceClass.DOOR,
            on_value="1",
            translation_key="door_open",
        ),
        HonBinarySensorEntityDescription(
            key="anticrease", name="Anti-Crease", translation_key="anti_crease"
        ),
    ),
    "OV": (
        HonBinarySensorEntityDescription(
            key="attributes.lastConnEvent.category",
            name="Connection",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            on_value="CONNECTED",
            icon="mdi:wifi",
            translation_key="connection",
        ),
        HonBinarySensorEntityDescription(
            key="attributes.parameters.onOffStatus",
            name="On",
            device_class=BinarySensorDeviceClass.RUNNING,
            on_value="1",
            icon="mdi:power-cycle",
            translation_key="on",
        ),
    ),
    "IH": (
        HonBinarySensorEntityDescription(
            key="attributes.lastConnEvent.category",
            name="Connection",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            on_value="CONNECTED",
            icon="mdi:wifi",
            translation_key="connection",
        ),
        HonBinarySensorEntityDescription(
            key="attributes.parameters.onOffStatus",
            name="On",
            device_class=BinarySensorDeviceClass.RUNNING,
            on_value="1",
            icon="mdi:power-cycle",
            translation_key="on",
        ),
        HonBinarySensorEntityDescription(
            key="hotStatus",
            name="Hot Status",
            device_class=BinarySensorDeviceClass.HEAT,
            on_value="1",
            translation_key="still_hot",
        ),
        HonBinarySensorEntityDescription(
            key="panStatus",
            name="Pan Status",
            on_value="1",
            icon="mdi:pot-mix",
            translation_key="pan_status",
        ),
        HonBinarySensorEntityDescription(
            key="hobLockStatus",
            name="Hob Lock",
            device_class=BinarySensorDeviceClass.LOCK,
            on_value="0",
            translation_key="child_lock",
        ),
    ),
    "DW": (
        HonBinarySensorEntityDescription(
            key="saltStatus",
            name="Salt",
            device_class=BinarySensorDeviceClass.PROBLEM,
            on_value="1",
            icon="mdi:shaker-outline",
            translation_key="salt_level",
        ),
        HonBinarySensorEntityDescription(
            key="rinseAidStatus",
            name="Rinse Aid",
            device_class=BinarySensorDeviceClass.PROBLEM,
            on_value="1",
            icon="mdi:spray-bottle",
            translation_key="rinse_aid",
        ),
        HonBinarySensorEntityDescription(
            key="attributes.lastConnEvent.category",
            name="Connection",
            device_class=BinarySensorDeviceClass.CONNECTIVITY,
            on_value="CONNECTED",
            translation_key="connection",
        ),
        HonBinarySensorEntityDescription(
            key="doorStatus",
            name="Door",
            device_class=BinarySensorDeviceClass.DOOR,
            on_value="1",
            translation_key="door_open",
        ),
    ),
    "AC": (
        HonBinarySensorEntityDescription(
            key="filterChangeStatusLocal",
            name="Filter Replacement",
            device_class=BinarySensorDeviceClass.PROBLEM,
            on_value="1",
            translation_key="filter_replacement",
        ),
        HonBinarySensorEntityDescription(
            key="ch2oCleaningStatus",
            name="Ch2O Cleaning",
            on_value="1",
        ),
    ),
    "REF": (
        HonBinarySensorEntityDescription(
            key="quickModeZ2",
            name="Super Cool",
            icon="mdi:snowflake",
            device_class=BinarySensorDeviceClass.RUNNING,
            on_value="1",
            translation_key="super_cool",
        ),
        HonBinarySensorEntityDescription(
            key="quickModeZ1",
            name="Super Freeze",
            icon="mdi:snowflake-variant",
            device_class=BinarySensorDeviceClass.RUNNING,
            on_value="1",
            translation_key="super_freeze",
        ),
        HonBinarySensorEntityDescription(
            key="doorStatusZ1",
            name="Door Status Freezer",
            device_class=BinarySensorDeviceClass.DOOR,
            icon="mdi:fridge-top",
            on_value="1",
            translation_key="freezer_door",
        ),
        HonBinarySensorEntityDescription(
            key="door2StatusZ1",
            name="Door Status Fridge",
            icon="mdi:fridge-bottom",
            device_class=BinarySensorDeviceClass.DOOR,
            on_value="1",
            translation_key="fridge_door",
        ),
        HonBinarySensorEntityDescription(
            key="intelligenceMode",
            name="Auto-Set Mode",
            icon="mdi:thermometer-auto",
            device_class=BinarySensorDeviceClass.RUNNING,
            on_value="1",
            translation_key="auto_set",
        ),
        HonBinarySensorEntityDescription(
            key="holidayMode",
            name="Holiday Mode",
            icon="mdi:palm-tree",
            device_class=BinarySensorDeviceClass.RUNNING,
            on_value="1",
            translation_key="holiday_mode",
        ),
    ),
}


BINARY_SENSORS["WD"] = unique_entities(BINARY_SENSORS["WM"], BINARY_SENSORS["TD"])


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities) -> None:
    entities = []
    for device in hass.data[DOMAIN][entry.unique_id].appliances:
        for description in BINARY_SENSORS.get(device.appliance_type, []):
            if not device.get(description.key):
                continue
            entity = HonBinarySensorEntity(hass, entry, device, description)
            await entity.coordinator.async_config_entry_first_refresh()
            entities.append(entity)
    async_add_entities(entities)


class HonBinarySensorEntity(HonEntity, BinarySensorEntity):
    entity_description: HonBinarySensorEntityDescription

    def __init__(self, hass, entry, device, description) -> None:
        super().__init__(hass, entry, device)

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
