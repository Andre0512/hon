import logging
from dataclasses import dataclass
from typing import Any

from homeassistant.components.switch import SwitchEntityDescription, SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import callback
from pyhon import Hon
from pyhon.appliance import HonAppliance
from pyhon.parameter.base import HonParameter
from pyhon.parameter.range import HonParameterRange

from .const import DOMAIN
from .hon import HonEntity, unique_entities, get_coordinator

_LOGGER = logging.getLogger(__name__)


@dataclass
class HonSwitchEntityDescriptionMixin:
    turn_on_key: str = ""
    turn_off_key: str = ""
    status_key: str = ""


@dataclass
class HonSwitchEntityDescription(
    HonSwitchEntityDescriptionMixin, SwitchEntityDescription
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
            translation_key="washing_machine",
        ),
        HonSwitchEntityDescription(
            key="pause",
            name="Pause Washing Machine",
            icon="mdi:pause",
            turn_on_key="pauseProgram",
            turn_off_key="resumeProgram",
            translation_key="pause",
        ),
        HonSwitchEntityDescription(
            key="startProgram.delayStatus",
            name="Delay Status",
            icon="mdi:timer-check",
            entity_category=EntityCategory.CONFIG,
            translation_key="delay_time",
        ),
        HonSwitchEntityDescription(
            key="startProgram.haier_SoakPrewashSelection",
            name="Soak Prewash Selection",
            icon="mdi:tshirt-crew",
            entity_category=EntityCategory.CONFIG,
            translation_key="prewash",
        ),
        HonSwitchEntityDescription(
            key="startProgram.permanentPressStatus",
            name="Keep Fresh",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:refresh-circle",
            translation_key="keep_fresh",
        ),
        HonSwitchEntityDescription(
            key="startProgram.autoSoftenerStatus",
            name="Auto Dose Softener",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:teddy-bear",
            translation_key="auto_dose_softener",
        ),
        HonSwitchEntityDescription(
            key="startProgram.autoDetergentStatus",
            name="Auto Dose Detergent",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:cup",
            translation_key="auto_dose_detergent",
        ),
        HonSwitchEntityDescription(
            key="startProgram.acquaplus",
            name="Acqua Plus",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:water-plus",
            translation_key="acqua_plus",
        ),
        HonSwitchEntityDescription(
            key="startProgram.extraRinse1",
            name="Extra Rinse 1",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:numeric-1-box-multiple-outline",
            translation_key="extra_rinse_1",
        ),
        HonSwitchEntityDescription(
            key="startProgram.extraRinse2",
            name="Extra Rinse 2",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:numeric-2-box-multiple-outline",
            translation_key="extra_rinse_2",
        ),
        HonSwitchEntityDescription(
            key="startProgram.extraRinse3",
            name="Extra Rinse 3",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:numeric-3-box-multiple-outline",
            translation_key="extra_rinse_3",
        ),
        HonSwitchEntityDescription(
            key="startProgram.goodNight",
            name="Good Night",
            icon="mdi:weather-night",
            entity_category=EntityCategory.CONFIG,
            translation_key="good_night",
        ),
    ),
    "TD": (
        HonSwitchEntityDescription(
            key="active",
            name="Tumble Dryer",
            icon="mdi:tumble-dryer",
            turn_on_key="startProgram",
            turn_off_key="stopProgram",
            translation_key="tumble_dryer",
        ),
        HonSwitchEntityDescription(
            key="pause",
            name="Pause Tumble Dryer",
            icon="mdi:pause",
            turn_on_key="pauseProgram",
            turn_off_key="resumeProgram",
            translation_key="pause",
        ),
        HonSwitchEntityDescription(
            key="startProgram.sterilizationStatus",
            name="Sterilization",
            icon="mdi:clock-start",
            entity_category=EntityCategory.CONFIG,
        ),
        HonSwitchEntityDescription(
            key="startProgram.antiCreaseTime",
            name="Anti-Crease",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:timer",
            translation_key="anti_crease",
        ),
        HonSwitchEntityDescription(
            key="startProgram.anticrease",
            name="Anti-Crease",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:timer",
            translation_key="anti_crease",
        ),
    ),
    "OV": (
        HonSwitchEntityDescription(
            key="active",
            name="Oven",
            icon="mdi:toaster-oven",
            turn_on_key="startProgram",
            turn_off_key="stopProgram",
            translation_key="oven",
        ),
        HonSwitchEntityDescription(
            key="startProgram.preheatStatus",
            name="Preheat",
            icon="mdi:thermometer-chevron-up",
            entity_category=EntityCategory.CONFIG,
            translation_key="preheat",
        ),
    ),
    "WD": (
        HonSwitchEntityDescription(
            key="active",
            name="Washer Dryer",
            icon="mdi:washing-machine",
            turn_on_key="startProgram",
            turn_off_key="stopProgram",
            translation_key="washer_dryer",
        ),
        HonSwitchEntityDescription(
            key="pause",
            name="Pause Washer Dryer",
            icon="mdi:pause",
            turn_on_key="pauseProgram",
            turn_off_key="resumeProgram",
            translation_key="pause",
        ),
    ),
    "DW": (
        HonSwitchEntityDescription(
            key="active",
            name="Dish Washer",
            icon="mdi:dishwasher",
            turn_on_key="startProgram",
            turn_off_key="stopProgram",
            translation_key="dish_washer",
        ),
        HonSwitchEntityDescription(
            key="startProgram.extraDry",
            name="Extra Dry",
            icon="mdi:hair-dryer",
            entity_category=EntityCategory.CONFIG,
            translation_key="extra_dry",
        ),
        HonSwitchEntityDescription(
            key="startProgram.halfLoad",
            name="Half Load",
            icon="mdi:fraction-one-half",
            entity_category=EntityCategory.CONFIG,
            translation_key="half_load",
        ),
        HonSwitchEntityDescription(
            key="startProgram.openDoor",
            name="Open Door",
            icon="mdi:door-open",
            entity_category=EntityCategory.CONFIG,
            translation_key="open_door",
        ),
        HonSwitchEntityDescription(
            key="startProgram.threeInOne",
            name="Three in One",
            icon="mdi:numeric-3-box-outline",
            entity_category=EntityCategory.CONFIG,
            translation_key="three_in_one",
        ),
        HonSwitchEntityDescription(
            key="startProgram.ecoExpress",
            name="Eco Express",
            icon="mdi:sprout",
            entity_category=EntityCategory.CONFIG,
            translation_key="eco",
        ),
        HonSwitchEntityDescription(
            key="startProgram.addDish",
            name="Add Dish",
            icon="mdi:silverware-fork-knife",
            entity_category=EntityCategory.CONFIG,
            translation_key="add_dish",
        ),
        HonSwitchEntityDescription(
            key="settings.buzzerDisabled",
            name="Buzzer Disabled",
            icon="mdi:volume-off",
            translation_key="buzzer",
        ),
    ),
    "AC": (
        HonSwitchEntityDescription(
            key="settings.10degreeHeatingStatus",
            status_key="10degreeHeatingStatus",
            name="10° Heating",
            icon="mdi:heat-wave",
            translation_key="10_degree_heating",
        ),
        HonSwitchEntityDescription(
            key="settings.echoStatus",
            status_key="echoStatus",
            name="Echo",
            icon="mdi:account-voice",
        ),
        HonSwitchEntityDescription(
            key="settings.ecoMode",
            name="Eco Mode",
            translation_key="eco_mode",
        ),
        HonSwitchEntityDescription(
            key="settings.healthMode",
            status_key="healthMode",
            name="Health Mode",
            icon="mdi:medication-outline",
        ),
        HonSwitchEntityDescription(
            key="settings.muteStatus",
            status_key="muteStatus",
            name="Mute",
            icon="mdi:volume-off",
            translation_key="mute_mode",
        ),
        HonSwitchEntityDescription(
            key="settings.rapidMode",
            status_key="rapidMode",
            name="Rapid Mode",
            icon="mdi:run-fast",
            translation_key="rapid_mode",
        ),
        HonSwitchEntityDescription(
            key="settings.screenDisplayStatus",
            status_key="screenDisplayStatus",
            name="Screen Display",
            icon="mdi:monitor-small",
        ),
        HonSwitchEntityDescription(
            key="settings.selfCleaning56Status",
            name="Self Cleaning 56",
            icon="mdi:air-filter",
            translation_key="self_clean_56",
        ),
        HonSwitchEntityDescription(
            key="settings.selfCleaningStatus",
            status_key="selfCleaningStatus",
            name="Self Cleaning",
            icon="mdi:air-filter",
            translation_key="self_clean",
        ),
        HonSwitchEntityDescription(
            key="settings.silentSleepStatus",
            status_key="silentSleepStatus",
            name="Silent Sleep",
            icon="mdi:bed",
            translation_key="silent_mode",
        ),
    ),
    "REF": (
        HonSwitchEntityDescription(
            key="settings.intelligenceMode",
            status_key="intelligenceMode",
            name="Auto-Set Mode",
            icon="mdi:thermometer-auto",
            translation_key="auto_set",
        ),
        HonSwitchEntityDescription(
            key="settings.quickModeZ1",
            status_key="quickModeZ1",
            name="Super Freeze",
            icon="mdi:snowflake-variant",
            translation_key="super_freeze",
        ),
        HonSwitchEntityDescription(
            key="settings.quickModeZ2",
            status_key="quickModeZ2",
            name="Super Cool",
            icon="mdi:snowflake",
            translation_key="super_cool",
        ),
        HonSwitchEntityDescription(
            key="settings.holidayMode",
            status_key="holidayMode",
            name="Holiday Mode",
            icon="mdi:palm-tree",
            translation_key="holiday_mode",
        ),
    ),
}

SWITCHES["WD"] = unique_entities(SWITCHES["WD"], SWITCHES["WM"])
SWITCHES["WD"] = unique_entities(SWITCHES["WD"], SWITCHES["TD"])


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities) -> None:
    hon: Hon = hass.data[DOMAIN][entry.unique_id]
    appliances = []
    for device in hon.appliances:
        coordinator = get_coordinator(hass, device)
        await coordinator.async_config_entry_first_refresh()

        if descriptions := SWITCHES.get(device.appliance_type):
            for description in descriptions:
                if description.entity_category == EntityCategory.CONFIG:
                    if description.key not in device.available_settings:
                        continue
                else:
                    if not any(
                        [
                            device.get(description.key) is not None,
                            description.turn_on_key in list(device.commands),
                            description.turn_off_key in list(device.commands),
                        ]
                    ):
                        continue
                appliances.extend(
                    [HonSwitchEntity(hass, coordinator, entry, device, description)]
                )

    async_add_entities(appliances)


class HonSwitchEntity(HonEntity, SwitchEntity):
    entity_description: HonSwitchEntityDescription

    def __init__(
        self,
        hass,
        coordinator,
        entry,
        device: HonAppliance,
        description: HonSwitchEntityDescription,
    ) -> None:
        super().__init__(hass, entry, coordinator, device)

        self.entity_description = description
        self._attr_unique_id = f"{super().unique_id}{description.key}"

    @property
    def is_on(self) -> bool | None:
        """Return True if entity is on."""
        if self.entity_category == EntityCategory.CONFIG:
            setting = self._device.settings[self.entity_description.key]
            return (
                setting.value == "1"
                or hasattr(setting, "min")
                and setting.value != setting.min
            )
        elif self.entity_description.status_key:
            return self._device.get(self.entity_description.status_key, "0") == "1"
        return self._device.get(self.entity_description.key, False)

    async def async_turn_on(self, **kwargs: Any) -> None:
        if (
            self.entity_category == EntityCategory.CONFIG
            or "settings." in self.entity_description.key
        ):
            setting = self._device.settings[self.entity_description.key]
            if not type(setting) == HonParameter:
                setting.value = (
                    setting.max if isinstance(setting, HonParameterRange) else "1"
                )
                self.async_write_ha_state()
                await self.coordinator.async_refresh()
                if "settings." in self.entity_description.key:
                    await self._device.commands["settings"].send()
        else:
            await self._device.commands[self.entity_description.turn_on_key].send()

    async def async_turn_off(self, **kwargs: Any) -> None:
        if (
            self.entity_category == EntityCategory.CONFIG
            or "settings." in self.entity_description.key
        ):
            setting = self._device.settings[self.entity_description.key]
            if not type(setting) == HonParameter:
                setting.value = (
                    setting.min if isinstance(setting, HonParameterRange) else "0"
                )
                self.async_write_ha_state()
                if "settings." in self.entity_description.key:
                    await self._device.commands["settings"].send()
                await self.coordinator.async_refresh()
        else:
            await self._device.commands[self.entity_description.turn_off_key].send()

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        if self.entity_category == EntityCategory.CONFIG:
            return super().available
        else:
            return (
                super().available
                and self._device.get("remoteCtrValid", "1") == "1"
                and self._device.get("attributes.lastConnEvent.category")
                != "DISCONNECTED"
            )

    @callback
    def _handle_coordinator_update(self):
        if self.entity_description.status_key:
            value = self._device.get(self.entity_description.status_key, "0")
        elif self.entity_category == EntityCategory.CONFIG:
            value = self._device.settings.get(self.entity_description.key, "0")
        else:
            return
        self._attr_state = value == "1"
        self.async_write_ha_state()
