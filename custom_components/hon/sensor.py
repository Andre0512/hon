import logging

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE
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
from pyhon import Hon

from . import const
from .const import DOMAIN
from .hon import HonCoordinator, HonEntity, unique_entities

_LOGGER = logging.getLogger(__name__)


SENSORS: dict[str, tuple[SensorEntityDescription, ...]] = {
    "WM": (
        SensorEntityDescription(
            key="prPhase",
            name="Program Phase",
            icon="mdi:washing-machine",
            device_class=SensorDeviceClass.ENUM,
            translation_key="program_phases_wm",
            options=list(const.WASHING_PR_PHASE),
        ),
        SensorEntityDescription(
            key="totalElectricityUsed",
            name="Total Power",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            translation_key="energy_total",
        ),
        SensorEntityDescription(
            key="totalWaterUsed",
            name="Total Water",
            device_class=SensorDeviceClass.WATER,
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=UnitOfVolume.LITERS,
            translation_key="water_total",
        ),
        SensorEntityDescription(
            key="totalWashCycle",
            name="Total Wash Cycle",
            state_class=SensorStateClass.TOTAL_INCREASING,
            icon="mdi:counter",
            translation_key="cycles_total",
        ),
        SensorEntityDescription(
            key="currentElectricityUsed",
            name="Current Electricity Used",
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.KILO_WATT,
            icon="mdi:lightning-bolt",
            translation_key="energy_current",
        ),
        SensorEntityDescription(
            key="currentWaterUsed",
            name="Current Water Used",
            state_class=SensorStateClass.MEASUREMENT,
            icon="mdi:water",
            translation_key="water_current",
        ),
        SensorEntityDescription(
            key="startProgram.weight",
            name="Suggested weight",
            state_class=SensorStateClass.MEASUREMENT,
            entity_category=EntityCategory.CONFIG,
            native_unit_of_measurement=UnitOfMass.KILOGRAMS,
            icon="mdi:weight-kilogram",
            translation_key="suggested_load",
        ),
        SensorEntityDescription(
            key="machMode",
            name="Machine Status",
            icon="mdi:information",
            device_class=SensorDeviceClass.ENUM,
            translation_key="washing_modes",
            options=list(const.MACH_MODE),
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
            translation_key="remaining_time",
        ),
        SensorEntityDescription(
            key="spinSpeed",
            name="Spin Speed",
            icon="mdi:speedometer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
            translation_key="spin_speed",
        ),
        SensorEntityDescription(
            key="startProgram.energyLabel",
            name="Energy Label",
            icon="mdi:lightning-bolt-circle",
            state_class=SensorStateClass.MEASUREMENT,
            entity_category=EntityCategory.CONFIG,
            translation_key="energy_label",
        ),
        SensorEntityDescription(
            key="startProgram.liquidDetergentDose",
            name="Liquid Detergent Dose",
            icon="mdi:cup-water",
            entity_category=EntityCategory.CONFIG,
            translation_key="det_liquid",
        ),
        SensorEntityDescription(
            key="startProgram.powderDetergentDose",
            name="Powder Detergent Dose",
            icon="mdi:cup",
            entity_category=EntityCategory.CONFIG,
            translation_key="det_dust",
        ),
        SensorEntityDescription(
            key="startProgram.remainingTime",
            name="Remaining Time",
            icon="mdi:timer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTime.MINUTES,
            entity_category=EntityCategory.CONFIG,
            translation_key="remaining_time",
        ),
        SensorEntityDescription(
            key="dirtyLevel",
            name="Dirt level",
            icon="mdi:liquid-spot",
            translation_key="dirt_level",
        ),
        SensorEntityDescription(
            key="startProgram.suggestedLoadW",
            name="Suggested Load",
            icon="mdi:weight-kilogram",
            entity_category=EntityCategory.CONFIG,
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfMass.KILOGRAMS,
            translation_key="suggested_load",
        ),
        SensorEntityDescription(
            key="temp",
            name="Current Temperature",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="temperature",
        ),
    ),
    "TD": (
        SensorEntityDescription(
            key="machMode",
            name="Machine Status",
            icon="mdi:information",
            device_class=SensorDeviceClass.ENUM,
            translation_key="washing_modes",
            options=list(const.MACH_MODE),
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
            translation_key="remaining_time",
        ),
        SensorEntityDescription(
            key="delayTime",
            name="Start Time",
            icon="mdi:clock-start",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="delay_time",
        ),
        SensorEntityDescription(
            key="programName",
            name="Program",
            icon="mdi:tumble-dryer",
            device_class=SensorDeviceClass.ENUM,
            translation_key="programs_td",
            options=const.PROGRAMS_TD,
        ),
        SensorEntityDescription(
            key="prPhase",
            name="Program Phase",
            icon="mdi:washing-machine",
            device_class=SensorDeviceClass.ENUM,
            translation_key="program_phases_td",
            options=list(const.TUMBLE_DRYER_PR_PHASE),
        ),
        SensorEntityDescription(
            key="dryLevel",
            name="Dry level",
            icon="mdi:hair-dryer",
            device_class=SensorDeviceClass.ENUM,
            translation_key="dry_levels",
            options=list(const.TUMBLE_DRYER_DRY_LEVEL),
        ),
        SensorEntityDescription(
            key="tempLevel",
            name="Temperature level",
            icon="mdi:thermometer",
            translation_key="tumbledryertemplevel",
        ),
        SensorEntityDescription(
            key="startProgram.suggestedLoadD",
            name="Suggested Load",
            icon="mdi:weight-kilogram",
            entity_category=EntityCategory.CONFIG,
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfMass.KILOGRAMS,
            translation_key="suggested_load",
        ),
        SensorEntityDescription(
            key="startProgram.energyLabel",
            name="Energy Label",
            icon="mdi:lightning-bolt-circle",
            state_class=SensorStateClass.MEASUREMENT,
            entity_category=EntityCategory.CONFIG,
            translation_key="energy_label",
        ),
        SensorEntityDescription(
            key="startProgram.steamLevel",
            name="Steam level",
            icon="mdi:smoke",
            entity_category=EntityCategory.CONFIG,
            translation_key="steam_level",
        ),
        SensorEntityDescription(
            key="steamLevel",
            name="Steam level",
            icon="mdi:smoke",
            translation_key="steam_level",
        ),
        SensorEntityDescription(
            key="steamType",
            name="Steam Type",
            icon="mdi:weather-dust",
            entity_category=EntityCategory.CONFIG,
        ),
    ),
    "OV": (
        SensorEntityDescription(
            key="remainingTimeMM",
            name="Remaining Time",
            icon="mdi:timer",
            native_unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="remaining_time",
        ),
        SensorEntityDescription(
            key="delayTime",
            name="Start Time",
            icon="mdi:clock-start",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="delay_time",
        ),
        SensorEntityDescription(
            key="temp",
            name="Temperature",
            icon="mdi:thermometer",
            translation_key="temperature",
        ),
        SensorEntityDescription(
            key="tempSel",
            name="Temperature Selected",
            icon="mdi:thermometer",
            translation_key="target_temperature",
        ),
    ),
    "IH": (
        SensorEntityDescription(
            key="remainingTimeMM",
            name="Remaining Time",
            icon="mdi:timer",
            native_unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="remaining_time",
        ),
        SensorEntityDescription(
            key="temp",
            name="Temperature",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="temperature",
        ),
        SensorEntityDescription(
            key="errors", name="Error", icon="mdi:math-log", translation_key="errors"
        ),
        SensorEntityDescription(
            key="power",
            name="Power",
            icon="mdi:lightning-bolt",
            state_class=SensorStateClass.MEASUREMENT,
            translation_key="power",
        ),
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
            translation_key="water_efficiency",
        ),
        SensorEntityDescription(
            key="startProgram.waterSaving",
            name="Water Saving",
            icon="mdi:water-percent",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=PERCENTAGE,
            entity_category=EntityCategory.CONFIG,
            translation_key="water_saving",
        ),
        SensorEntityDescription(
            key="startProgram.temp",
            name="Temperature",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            entity_category=EntityCategory.CONFIG,
            translation_key="temperature",
        ),
        SensorEntityDescription(
            key="startProgram.energyLabel",
            name="Energy Label",
            icon="mdi:lightning-bolt-circle",
            state_class=SensorStateClass.MEASUREMENT,
            entity_category=EntityCategory.CONFIG,
            translation_key="energy_label",
        ),
        SensorEntityDescription(
            key="startProgram.remainingTime",
            name="Time",
            icon="mdi:timer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTime.MINUTES,
            entity_category=EntityCategory.CONFIG,
            translation_key="duration",
        ),
        SensorEntityDescription(
            key="machMode",
            name="Machine Status",
            icon="mdi:information",
            device_class=SensorDeviceClass.ENUM,
            translation_key="washing_modes",
            options=list(const.MACH_MODE),
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
            translation_key="remaining_time",
        ),
        SensorEntityDescription(
            key="prPhase",
            name="Program Phase",
            icon="mdi:washing-machine",
            device_class=SensorDeviceClass.ENUM,
            translation_key="program_phases_dw",
            options=list(const.DISHWASHER_PR_PHASE),
        ),
    ),
    "REF": (
        SensorEntityDescription(
            key="humidityEnv",
            name="Room Humidity",
            icon="mdi:water-percent",
            device_class=SensorDeviceClass.HUMIDITY,
            native_unit_of_measurement=PERCENTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            translation_key="humidity",
        ),
        SensorEntityDescription(
            key="tempEnv",
            name="Room Temperature",
            icon="mdi:home-thermometer-outline",
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="room_temperature",
        ),
        SensorEntityDescription(
            key="tempZ1",
            name="Temperature Fridge",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="fridge_temp",
        ),
        SensorEntityDescription(
            key="tempZ2",
            name="Temperature Freezer",
            icon="mdi:snowflake-thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="freezer_temp",
        ),
    ),
}
SENSORS["WD"] = unique_entities(SENSORS["WM"], SENSORS["TD"])


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
                if not device.get(description.key) and not device.settings.get(
                    description.key
                ):
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
        value = self._device.get(self.entity_description.key, "")
        if not value and self.entity_description.state_class is not None:
            return 0
        return value

    @callback
    def _handle_coordinator_update(self):
        value = self._device.get(self.entity_description.key, "")
        if not value and self.entity_description.state_class is not None:
            self._attr_native_value = 0
        self._attr_native_value = value
        self.async_write_ha_state()
