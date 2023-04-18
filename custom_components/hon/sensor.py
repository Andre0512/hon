import logging

from pyhon import Hon

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    REVOLUTIONS_PER_MINUTE,
    UnitOfEnergy,
    UnitOfVolume,
    UnitOfMass,
    UnitOfPower,
    UnitOfTime,
    UnitOfTemperature,
)
from homeassistant.core import callback
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.typing import StateType
from homeassistant.const import PERCENTAGE

from .const import DOMAIN
from .hon import HonCoordinator, HonEntity

_LOGGER = logging.getLogger(__name__)

SENSORS: dict[str, tuple[SensorEntityDescription, ...]] = {
    "WM": (
        SensorEntityDescription(
            key="totalElectricityUsed",
            name="Total Power",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        ),
        SensorEntityDescription(
            key="totalWaterUsed",
            name="Total Water",
            device_class=SensorDeviceClass.WATER,
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=UnitOfVolume.LITERS,
        ),
        SensorEntityDescription(
            key="totalWashCycle",
            name="Total Wash Cycle",
            state_class=SensorStateClass.TOTAL_INCREASING,
            icon="mdi:counter",
        ),
        SensorEntityDescription(
            key="currentElectricityUsed",
            name="Current Electricity Used",
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.KILO_WATT_HOUR,
            icon="mdi:lightning-bolt",
        ),
        SensorEntityDescription(
            key="currentWaterUsed",
            name="Current Water Used",
            state_class=SensorStateClass.MEASUREMENT,
            icon="mdi:water",
        ),
        SensorEntityDescription(
            key="startProgram.weight",
            name="Suggested weight",
            state_class=SensorStateClass.MEASUREMENT,
            entity_category=EntityCategory.CONFIG,
            native_unit_of_measurement=UnitOfMass.KILOGRAMS,
            icon="mdi:weight-kilogram",
        ),
        SensorEntityDescription(
            key="machMode",
            name="Machine Status",
            icon="mdi:information",
            translation_key="mode",
        ),
        SensorEntityDescription(
            key="errors", name="Error", icon="mdi:math-log", translation_key="errors"
        ),
        SensorEntityDescription(
            key="remainingTimeMM",
            name="Remaining Time",
            icon="mdi:timer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTime.MINUTES,
        ),
        SensorEntityDescription(
            key="spinSpeed",
            name="Spin Speed",
            icon="mdi:speedometer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTime.MINUTES,
        ),
    ),
    "TD": (
        SensorEntityDescription(
            key="machMode",
            name="Machine Status",
            icon="mdi:information",
            translation_key="mode",
        ),
        SensorEntityDescription(
            key="errors", name="Error", icon="mdi:math-log", translation_key="errors"
        ),
        SensorEntityDescription(
            key="remainingTimeMM",
            name="Remaining Time",
            icon="mdi:timer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTime.MINUTES,
        ),
        SensorEntityDescription(
            key="delayTime",
            name="Start Time",
            icon="mdi:clock-start",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTime.MINUTES,
        ),
        SensorEntityDescription(
            key="prCode",
            name="Program",
            icon="mdi:tumble-dryer",
            translation_key="tumbledryerprogram",
        ),
        SensorEntityDescription(
            key="prPhase",
            name="Program Phase",
            icon="mdi:tumble-dryer",
            translation_key="tumbledryerprogramphase",
        ),
        SensorEntityDescription(
            key="dryLevel",
            name="Dry level",
            icon="mdi:hair-dryer",
            translation_key="tumbledryerdrylevel",
        ),
        SensorEntityDescription(
            key="tempLevel",
            name="Temperature level",
            icon="mdi:thermometer",
            translation_key="tumbledryertemplevel",
        ),
    ),
    "WD": (
        SensorEntityDescription(
            key="totalElectricityUsed",
            name="Total Power",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        ),
        SensorEntityDescription(
            key="totalWaterUsed",
            name="Total Water",
            device_class=SensorDeviceClass.WATER,
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=UnitOfVolume.LITERS,
        ),
        SensorEntityDescription(
            key="totalWashCycle",
            name="Total Wash Cycle",
            state_class=SensorStateClass.TOTAL_INCREASING,
            icon="mdi:counter",
        ),
        SensorEntityDescription(
            key="currentElectricityUsed",
            name="Current Electricity Used",
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.KILO_WATT_HOUR,
            icon="mdi:lightning-bolt",
        ),
        SensorEntityDescription(
            key="currentWaterUsed",
            name="Current Water Used",
            state_class=SensorStateClass.MEASUREMENT,
            icon="mdi:water",
        ),
        SensorEntityDescription(
            key="startProgram.weight",
            name="Suggested weight",
            state_class=SensorStateClass.MEASUREMENT,
            entity_category=EntityCategory.CONFIG,
            native_unit_of_measurement=UnitOfMass.KILOGRAMS,
            icon="mdi:weight-kilogram",
        ),
        SensorEntityDescription(
            key="machMode",
            name="Machine Status",
            icon="mdi:information",
            translation_key="mode",
        ),
        SensorEntityDescription(
            key="spinSpeed",
            name="Spin Speed",
            icon="mdi:fast-forward-outline",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
        ),
        SensorEntityDescription(
            key="remainingTimeMM",
            name="Remaining Time",
            icon="mdi:timer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTime.MINUTES,
        ),
        SensorEntityDescription(
            key="prCode",
            name="Current Program",
            icon="mdi:tumble-dryer",
        ),
        SensorEntityDescription(
            key="prPhase",
            name="Program Phase",
            icon="mdi:tumble-dryer",
        ),
        SensorEntityDescription(
            key="dryLevel",
            name="Dry level",
            icon="mdi:hair-dryer",
        ),
        SensorEntityDescription(
            key="dirtyLevel",
            name="Dirt level",
            icon="mdi:liquid-spot",
        ),
        SensorEntityDescription(
            key="steamLevel",
            name="Steam level",
            icon="mdi:smoke",
        ),
        SensorEntityDescription(
            key="temp",
            name="Current Temperature",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        ),
    ),
    "OV": (
        SensorEntityDescription(
            key="remainingTimeMM",
            name="Remaining Time",
            icon="mdi:timer",
            native_unit_of_measurement=UnitOfTime.MINUTES,
        ),
        SensorEntityDescription(
            key="delayTime",
            name="Start Time",
            icon="mdi:clock-start",
        ),
        SensorEntityDescription(
            key="temp",
            name="Temperature",
            icon="mdi:thermometer",
        ),
        SensorEntityDescription(
            key="tempSel",
            name="Temperature Selected",
            icon="mdi:thermometer",
        ),
    ),
    "IH": (
        SensorEntityDescription(
            key="remainingTimeMM",
            name="Remaining Time",
            icon="mdi:timer",
            native_unit_of_measurement=UnitOfTime.MINUTES,
        ),
        SensorEntityDescription(
            key="temp",
            name="Temperature",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        ),
        SensorEntityDescription(key="errors", name="Error", icon="mdi:math-log"),
    ),
    "DW": (
        SensorEntityDescription(
            key="startProgram.ecoIndex",
            name="Eco Index",
            icon="mdi:sprout",
            state_class=SensorStateClass.MEASUREMENT,
            entity_category=EntityCategory.CONFIG,
        ),
        SensorEntityDescription(
            key="startProgram.waterEfficiency",
            name="Water Efficiency",
            icon="mdi:water",
            state_class=SensorStateClass.MEASUREMENT,
            entity_category=EntityCategory.CONFIG,
        ),
        SensorEntityDescription(
            key="startProgram.waterSaving",
            name="Water Saving",
            icon="mdi:water-percent",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=PERCENTAGE,
            entity_category=EntityCategory.CONFIG,
        ),
        SensorEntityDescription(
            key="startProgram.temp",
            name="Temperature",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            entity_category=EntityCategory.CONFIG,
        ),
        SensorEntityDescription(
            key="startProgram.energyLabel",
            name="Energy Label",
            icon="mdi:lightning-bolt-circle",
            state_class=SensorStateClass.MEASUREMENT,
            entity_category=EntityCategory.CONFIG,
        ),
        SensorEntityDescription(
            key="startProgram.remainingTime",
            name="Time",
            icon="mdi:timer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTime.MINUTES,
            entity_category=EntityCategory.CONFIG,
        ),
        SensorEntityDescription(
            key="machMode",
            name="Machine Status",
            icon="mdi:information",
            translation_key="mode_dw",
        ),
        SensorEntityDescription(
            key="errors", name="Error", icon="mdi:math-log", translation_key="errors"
        ),
        SensorEntityDescription(
            key="remainingTimeMM",
            name="Remaining Time",
            icon="mdi:timer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTime.MINUTES,
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

        if descriptions := SENSORS.get(device.appliance_type):
            for description in descriptions:
                if not device.get(description.key):
                    _LOGGER.warning(
                        "[%s] Can't setup %s", device.appliance_type, description.key
                    )
                    continue
                appliances.extend(
                    [HonSensorEntity(hass, coordinator, entry, device, description)]
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
        return self._device.get(self.entity_description.key, "")

    @callback
    def _handle_coordinator_update(self):
        self._attr_native_value = self._device.get(self.entity_description.key, "")
        self.async_write_ha_state()
