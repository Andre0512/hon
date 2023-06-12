import logging
from dataclasses import dataclass
from typing import Dict

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

from . import const
from .const import DOMAIN
from .hon import HonEntity, unique_entities, get_readable

_LOGGER = logging.getLogger(__name__)


@dataclass
class HonConfigSensorEntityDescription(SensorEntityDescription):
    entity_category: EntityCategory = EntityCategory.CONFIG
    option_list: Dict[int, str] = None


@dataclass
class HonSensorEntityDescription(SensorEntityDescription):
    option_list: Dict[int, str] = None


SENSORS: dict[str, tuple[SensorEntityDescription, ...]] = {
    "WM": (
        HonSensorEntityDescription(
            key="prPhase",
            name="Program Phase",
            icon="mdi:washing-machine",
            device_class=SensorDeviceClass.ENUM,
            translation_key="program_phases_wm",
            option_list=const.WASHING_PR_PHASE,
        ),
        HonSensorEntityDescription(
            key="totalElectricityUsed",
            name="Total Power",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            translation_key="energy_total",
        ),
        HonSensorEntityDescription(
            key="totalWaterUsed",
            name="Total Water",
            device_class=SensorDeviceClass.WATER,
            state_class=SensorStateClass.TOTAL_INCREASING,
            native_unit_of_measurement=UnitOfVolume.LITERS,
            translation_key="water_total",
        ),
        HonSensorEntityDescription(
            key="totalWashCycle",
            name="Total Wash Cycle",
            state_class=SensorStateClass.TOTAL_INCREASING,
            icon="mdi:counter",
            translation_key="cycles_total",
        ),
        HonSensorEntityDescription(
            key="currentElectricityUsed",
            name="Current Electricity Used",
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.POWER,
            native_unit_of_measurement=UnitOfPower.KILO_WATT,
            icon="mdi:lightning-bolt",
            translation_key="energy_current",
        ),
        HonSensorEntityDescription(
            key="currentWaterUsed",
            name="Current Water Used",
            state_class=SensorStateClass.MEASUREMENT,
            icon="mdi:water",
            translation_key="water_current",
        ),
        HonConfigSensorEntityDescription(
            key="startProgram.weight",
            name="Suggested weight",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfMass.KILOGRAMS,
            icon="mdi:weight-kilogram",
            translation_key="suggested_load",
        ),
        HonSensorEntityDescription(
            key="machMode",
            name="Machine Status",
            icon="mdi:information",
            device_class=SensorDeviceClass.ENUM,
            translation_key="washing_modes",
            option_list=const.MACH_MODE,
        ),
        HonSensorEntityDescription(
            key="errors", name="Error", icon="mdi:math-log", translation_key="errors"
        ),
        HonSensorEntityDescription(
            key="remainingTimeMM",
            name="Remaining Time",
            icon="mdi:timer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="remaining_time",
        ),
        HonSensorEntityDescription(
            key="spinSpeed",
            name="Spin Speed",
            icon="mdi:speedometer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=REVOLUTIONS_PER_MINUTE,
            translation_key="spin_speed",
        ),
        HonConfigSensorEntityDescription(
            key="startProgram.energyLabel",
            name="Energy Label",
            icon="mdi:lightning-bolt-circle",
            state_class=SensorStateClass.MEASUREMENT,
            translation_key="energy_label",
        ),
        HonConfigSensorEntityDescription(
            key="startProgram.liquidDetergentDose",
            name="Liquid Detergent Dose",
            icon="mdi:cup-water",
            translation_key="det_liquid",
        ),
        HonConfigSensorEntityDescription(
            key="startProgram.powderDetergentDose",
            name="Powder Detergent Dose",
            icon="mdi:cup",
            translation_key="det_dust",
        ),
        HonConfigSensorEntityDescription(
            key="startProgram.remainingTime",
            name="Remaining Time",
            icon="mdi:timer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="remaining_time",
        ),
        HonSensorEntityDescription(
            key="dirtyLevel",
            name="Dirt level",
            icon="mdi:liquid-spot",
            device_class=SensorDeviceClass.ENUM,
            translation_key="dirt_level",
            option_list=const.DIRTY_LEVEL,
        ),
        HonConfigSensorEntityDescription(
            key="startProgram.suggestedLoadW",
            name="Suggested Load",
            icon="mdi:weight-kilogram",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfMass.KILOGRAMS,
            translation_key="suggested_load",
        ),
        HonSensorEntityDescription(
            key="temp",
            name="Current Temperature",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="temperature",
        ),
        HonSensorEntityDescription(
            key="programName",
            name="Program",
            icon="mdi:play",
            device_class=SensorDeviceClass.ENUM,
            translation_key="programs_wm",
        ),
    ),
    "TD": (
        HonSensorEntityDescription(
            key="machMode",
            name="Machine Status",
            icon="mdi:information",
            device_class=SensorDeviceClass.ENUM,
            translation_key="washing_modes",
            option_list=const.MACH_MODE,
        ),
        HonSensorEntityDescription(
            key="errors", name="Error", icon="mdi:math-log", translation_key="errors"
        ),
        HonSensorEntityDescription(
            key="remainingTimeMM",
            name="Remaining Time",
            icon="mdi:timer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="remaining_time",
        ),
        HonSensorEntityDescription(
            key="delayTime",
            name="Start Time",
            icon="mdi:clock-start",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="delay_time",
        ),
        HonSensorEntityDescription(
            key="programName",
            name="Program",
            icon="mdi:play",
            device_class=SensorDeviceClass.ENUM,
            translation_key="programs_td",
        ),
        HonSensorEntityDescription(
            key="prPhase",
            name="Program Phase",
            icon="mdi:washing-machine",
            device_class=SensorDeviceClass.ENUM,
            translation_key="program_phases_td",
            option_list=const.TUMBLE_DRYER_PR_PHASE,
        ),
        HonSensorEntityDescription(
            key="dryLevel",
            name="Dry level",
            icon="mdi:hair-dryer",
            device_class=SensorDeviceClass.ENUM,
            translation_key="dry_levels",
            option_list=const.TUMBLE_DRYER_DRY_LEVEL,
        ),
        HonSensorEntityDescription(
            key="tempLevel",
            name="Temperature level",
            icon="mdi:thermometer",
            translation_key="tumbledryertemplevel",
        ),
        HonConfigSensorEntityDescription(
            key="startProgram.suggestedLoadD",
            name="Suggested Load",
            icon="mdi:weight-kilogram",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfMass.KILOGRAMS,
            translation_key="suggested_load",
        ),
        HonConfigSensorEntityDescription(
            key="startProgram.energyLabel",
            name="Energy Label",
            icon="mdi:lightning-bolt-circle",
            state_class=SensorStateClass.MEASUREMENT,
            translation_key="energy_label",
        ),
        HonConfigSensorEntityDescription(
            key="startProgram.steamLevel",
            name="Steam level",
            device_class=SensorDeviceClass.ENUM,
            icon="mdi:smoke",
            translation_key="steam_level",
            option_list=const.STEAM_LEVEL,
        ),
        HonSensorEntityDescription(
            key="steamLevel",
            name="Steam level",
            icon="mdi:smoke",
            device_class=SensorDeviceClass.ENUM,
            translation_key="steam_level",
            option_list=const.STEAM_LEVEL,
        ),
        HonConfigSensorEntityDescription(
            key="steamType",
            name="Steam Type",
            icon="mdi:weather-dust",
        ),
    ),
    "OV": (
        HonSensorEntityDescription(
            key="remainingTimeMM",
            name="Remaining Time",
            icon="mdi:timer",
            native_unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="remaining_time",
        ),
        HonSensorEntityDescription(
            key="delayTime",
            name="Start Time",
            icon="mdi:clock-start",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="delay_time",
        ),
        HonSensorEntityDescription(
            key="temp",
            name="Temperature",
            icon="mdi:thermometer",
            translation_key="temperature",
        ),
        HonSensorEntityDescription(
            key="tempSel",
            name="Temperature Selected",
            icon="mdi:thermometer",
            translation_key="target_temperature",
        ),
        HonSensorEntityDescription(
            key="programName",
            name="Program",
            icon="mdi:play",
            device_class=SensorDeviceClass.ENUM,
            translation_key="programs_ov",
        ),
    ),
    "IH": (
        HonSensorEntityDescription(
            key="remainingTimeMM",
            name="Remaining Time",
            icon="mdi:timer",
            native_unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="remaining_time",
        ),
        HonSensorEntityDescription(
            key="temp",
            name="Temperature",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="temperature",
        ),
        HonSensorEntityDescription(
            key="errors", name="Error", icon="mdi:math-log", translation_key="errors"
        ),
        HonSensorEntityDescription(
            key="power",
            name="Power",
            icon="mdi:lightning-bolt",
            state_class=SensorStateClass.MEASUREMENT,
            translation_key="power",
        ),
        HonSensorEntityDescription(
            key="programName",
            name="Program",
            icon="mdi:play",
            device_class=SensorDeviceClass.ENUM,
            translation_key="programs_ih",
        ),
    ),
    "DW": (
        HonConfigSensorEntityDescription(
            key="startProgram.ecoIndex",
            name="Eco Index",
            icon="mdi:sprout",
            state_class=SensorStateClass.MEASUREMENT,
        ),
        HonConfigSensorEntityDescription(
            key="startProgram.waterEfficiency",
            name="Water Efficiency",
            icon="mdi:water",
            state_class=SensorStateClass.MEASUREMENT,
            translation_key="water_efficiency",
        ),
        HonConfigSensorEntityDescription(
            key="startProgram.waterSaving",
            name="Water Saving",
            icon="mdi:water-percent",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=PERCENTAGE,
            translation_key="water_saving",
        ),
        HonConfigSensorEntityDescription(
            key="startProgram.temp",
            name="Temperature",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="temperature",
        ),
        HonConfigSensorEntityDescription(
            key="startProgram.energyLabel",
            name="Energy Label",
            icon="mdi:lightning-bolt-circle",
            state_class=SensorStateClass.MEASUREMENT,
            translation_key="energy_label",
        ),
        HonConfigSensorEntityDescription(
            key="startProgram.remainingTime",
            name="Time",
            icon="mdi:timer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="duration",
        ),
        HonSensorEntityDescription(
            key="machMode",
            name="Machine Status",
            icon="mdi:information",
            device_class=SensorDeviceClass.ENUM,
            translation_key="washing_modes",
            option_list=const.MACH_MODE,
        ),
        HonSensorEntityDescription(
            key="errors", name="Error", icon="mdi:math-log", translation_key="errors"
        ),
        HonSensorEntityDescription(
            key="remainingTimeMM",
            name="Remaining Time",
            icon="mdi:timer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTime.MINUTES,
            translation_key="remaining_time",
        ),
        HonSensorEntityDescription(
            key="prPhase",
            name="Program Phase",
            icon="mdi:washing-machine",
            device_class=SensorDeviceClass.ENUM,
            translation_key="program_phases_dw",
            option_list=const.DISHWASHER_PR_PHASE,
        ),
        HonSensorEntityDescription(
            key="programName",
            name="Program",
            icon="mdi:play",
            device_class=SensorDeviceClass.ENUM,
            translation_key="programs_dw",
        ),
    ),
    "AC": (
        HonSensorEntityDescription(
            key="tempAirOutdoor",
            name="Air Temperature Outdoor",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        ),
        HonSensorEntityDescription(
            key="tempCoilerIndoor",
            name="Coiler Temperature Indoor",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        ),
        HonSensorEntityDescription(
            key="tempCoilerOutdoor",
            name="Coiler Temperature Outside",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        ),
        HonSensorEntityDescription(
            key="tempDefrostOutdoor",
            name="Defrost Temperature Outdoor",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        ),
        HonSensorEntityDescription(
            key="tempInAirOutdoor",
            name="In Air Temperature Outdoor",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        ),
        HonSensorEntityDescription(
            key="tempIndoor",
            name="Indoor Temperature",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        ),
        HonSensorEntityDescription(
            key="tempOutdoor",
            name="Outdoor Temperature",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        ),
        HonSensorEntityDescription(
            key="tempSel",
            name="Selected Temperature",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="target_temperature",
        ),
        HonSensorEntityDescription(
            key="programName",
            name="Program",
            icon="mdi:play",
            device_class=SensorDeviceClass.ENUM,
            translation_key="programs_ac",
        ),
        HonSensorEntityDescription(
            key="machMode",
            name="Machine Status",
            icon="mdi:information",
            device_class=SensorDeviceClass.ENUM,
            translation_key="mach_modes_ac",
            option_list=const.AC_MACH_MODE,
        ),
    ),
    "REF": (
        HonSensorEntityDescription(
            key="humidityEnv",
            name="Room Humidity",
            icon="mdi:water-percent",
            device_class=SensorDeviceClass.HUMIDITY,
            native_unit_of_measurement=PERCENTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            translation_key="humidity",
        ),
        HonSensorEntityDescription(
            key="tempEnv",
            name="Room Temperature",
            icon="mdi:home-thermometer-outline",
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="room_temperature",
        ),
        HonSensorEntityDescription(
            key="tempZ1",
            name="Temperature Fridge",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="fridge_temp",
        ),
        HonSensorEntityDescription(
            key="tempZ2",
            name="Temperature Freezer",
            icon="mdi:snowflake-thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="freezer_temp",
        ),
        HonSensorEntityDescription(
            key="errors", name="Error", icon="mdi:math-log", translation_key="errors"
        ),
    ),
    "HO": (
        HonSensorEntityDescription(
            key="delayTime",
            name="Delay time",
            icon="mdi:clock-start",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTime.MINUTES,
        ),
        HonSensorEntityDescription(
            key="delayTimeStatus",
            name="Delay time status",
            icon="mdi:clock-start",
        ),
        HonSensorEntityDescription(
            key="errors",
            name="Errors",
            icon="mdi:alert-circle",
        ),
        HonSensorEntityDescription(
            key="filterCleaningAlarmStatus",
            name="Filter Cleaning Alarm Status",
        ),
        HonSensorEntityDescription(
            key="filterCleaningStatus",
            name="Filter Cleaning Status",
        ),
        HonSensorEntityDescription(
            key="lastWorkTime",
            name="Last Work Time",
            icon="mdi:clock-start",
        ),
        HonSensorEntityDescription(
            key="lightStatus",
            name="Light Status",
            icon="mdi:lightbulb",
        ),
        HonSensorEntityDescription(
            key="machMode",
            name="Mach Mode",
        ),
        HonSensorEntityDescription(
            key="onOffStatus",
            name="On / Off Status",
            icon="mdi:lightbulb",
        ),
        HonSensorEntityDescription(
            key="quickDelayTimeStatus",
            name="Quick Delay Time Status",
        ),
        HonSensorEntityDescription(
            key="rgbLightColors",
            name="RGB Light Color",
            icon="mdi:lightbulb",
        ),
        HonSensorEntityDescription(
            key="rgbLightStatus",
            name="RGB Light Status",
            icon="mdi:lightbulb",
        ),
    ),
    "WC": (
        HonSensorEntityDescription(
            key="errors", name="Error", icon="mdi:math-log", translation_key="errors"
        ),
        HonSensorEntityDescription(
            key="humidityZ1",
            name="Humidity",
            icon="mdi:water-percent",
            device_class=SensorDeviceClass.HUMIDITY,
            native_unit_of_measurement=PERCENTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            translation_key="humidity",
        ),
        HonSensorEntityDescription(
            key="humidityZ2",
            name="Humidity 2",
            icon="mdi:water-percent",
            device_class=SensorDeviceClass.HUMIDITY,
            native_unit_of_measurement=PERCENTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            translation_key="humidity",
        ),
        HonSensorEntityDescription(
            key="temp",
            name="Temperature",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="temperature",
        ),
        HonSensorEntityDescription(
            key="tempEnv",
            name="Room Temperature",
            icon="mdi:home-thermometer-outline",
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="room_temperature",
        ),
        HonSensorEntityDescription(
            key="tempSel",
            name="Selected Temperature",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="target_temperature",
        ),
        HonSensorEntityDescription(
            key="tempSelZ2",
            name="Selected Temperature 2",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            device_class=SensorDeviceClass.TEMPERATURE,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="target_temperature",
        ),
        HonSensorEntityDescription(
            key="tempZ2",
            name="Temperature 2",
            icon="mdi:thermometer",
            state_class=SensorStateClass.MEASUREMENT,
            native_unit_of_measurement=UnitOfTemperature.CELSIUS,
            translation_key="temperature",
        ),
        HonSensorEntityDescription(
            key="programName",
            name="Program",
            icon="mdi:play",
            device_class=SensorDeviceClass.ENUM,
            translation_key="programs_wc",
        ),
    ),
}
SENSORS["WD"] = unique_entities(SENSORS["WM"], SENSORS["TD"])


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities) -> None:
    entities = []
    for device in hass.data[DOMAIN][entry.unique_id].appliances:
        for description in SENSORS.get(device.appliance_type, []):
            if isinstance(description, HonSensorEntityDescription):
                if device.get(description.key) is None:
                    continue
                entity = HonSensorEntity(hass, entry, device, description)
            elif isinstance(description, HonConfigSensorEntityDescription):
                if description.key not in device.available_settings:
                    continue
                entity = HonConfigSensorEntity(hass, entry, device, description)
            else:
                continue
            await entity.coordinator.async_config_entry_first_refresh()
            entities.append(entity)

    async_add_entities(entities)


class HonSensorEntity(HonEntity, SensorEntity):
    entity_description: HonSensorEntityDescription

    @callback
    def _handle_coordinator_update(self, update=True) -> None:
        value = self._device.get(self.entity_description.key, "")
        if self.entity_description.key == "programName":
            self._attr_options = self._device.settings.get(
                "startProgram.program"
            ).values + ["No Program"]
        elif self.entity_description.option_list is not None:
            self._attr_options = list(self.entity_description.option_list.values())
            value = get_readable(self.entity_description, value)
        if not value and self.entity_description.state_class is not None:
            self._attr_native_value = 0
        self._attr_native_value = value
        if update:
            self.async_write_ha_state()


class HonConfigSensorEntity(HonEntity, SensorEntity):
    entity_description: HonConfigSensorEntityDescription

    @callback
    def _handle_coordinator_update(self, update=True) -> None:
        value = self._device.settings.get(self.entity_description.key, None)
        if self.entity_description.state_class is not None:
            if value and value.value:
                value = (
                    float(value.value) if "." in str(value.value) else int(value.value)
                )
            else:
                value = 0
        else:
            value = value.value
        if self.entity_description.option_list is not None and not value == 0:
            self._attr_options = list(self.entity_description.option_list.values())
            value = get_readable(self.entity_description, value)
        self._attr_native_value = value
        if update:
            self.async_write_ha_state()
