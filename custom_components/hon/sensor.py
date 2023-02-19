import logging

from pyhon import HonConnection

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.typing import StateType
from custom_components import HonCoordinator
from .const import DOMAIN
from custom_components.hon import HonEntity

_LOGGER = logging.getLogger(__name__)

SENSORS: dict[str, tuple[SensorEntityDescription, ...]] = {
    "WM": (
        SensorEntityDescription(
            key="totalElectricityUsed",
            name="Total Power",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        SensorEntityDescription(
            key="totalWaterUsed",
            name="Total Water",
            device_class=SensorDeviceClass.WATER,
            state_class=SensorStateClass.TOTAL_INCREASING,
        ),
        SensorEntityDescription(
            key="totalWashCycle",
            name="Total Wash Cycle",
            state_class=SensorStateClass.TOTAL_INCREASING,
            icon="mdi:counter"
        ),
        SensorEntityDescription(
            key="currentElectricityUsed",
            name="Current Electricity Used",
            state_class=SensorStateClass.MEASUREMENT,
            icon="mdi:lightning-bolt"
        ),
        SensorEntityDescription(
            key="currentWaterUsed",
            name="Current Water Used",
            state_class=SensorStateClass.MEASUREMENT,
            icon="mdi:water"
        ),
    )
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

        if descriptions := SENSORS.get(device.appliance_type_name):
            for description in descriptions:
                appliances.extend([
                    HonSensorEntity(hass, coordinator, entry, device, description)]
                )

    async_add_entities(appliances)


class HonSensorEntity(HonEntity, SensorEntity):
    def __init__(self, hass, coordinator, entry, device, description) -> None:
        super().__init__(hass, entry, coordinator, device)

        self._coordinator = coordinator

        self.entity_description = description
        self._attr_unique_id = f"{super().unique_id}{description.key}"

    @property
    def native_value(self) -> StateType:
        return self._device.attributes.get(self.entity_description.key, "")

    @callback
    def _handle_coordinator_update(self):
        self._attr_native_value = self._device.attributes.get(self.entity_description.key, "")
        self.async_write_ha_state()
