#!/usr/bin/env python

import asyncio
import json
import re
import sys
from pathlib import Path

from pyhon import HonAPI

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from custom_components.hon import const

SENSOR = {
    "washing_modes": const.MACH_MODE,
    "mach_modes_ac": const.AC_MACH_MODE,
    "program_phases_wm": const.WASHING_PR_PHASE,
    "program_phases_td": const.TUMBLE_DRYER_PR_PHASE,
    "program_phases_dw": const.DISHWASHER_PR_PHASE,
    "dry_levels": const.TUMBLE_DRYER_DRY_LEVEL,
}

SELECT = {
    "dry_levels": const.TUMBLE_DRYER_DRY_LEVEL,
    "eco_pilot": const.AC_HUMAN_SENSE,
    "fan_mode": const.AC_FAN_MODE,
}

PROGRAMS = {
    "select": {
        "programs_ac": "PROGRAMS.AC",
        "programs_dw": "PROGRAMS.DW",
        "programs_ih": "PROGRAMS.IH",
        "programs_ov": "PROGRAMS.OV",
        "programs_td": "PROGRAMS.TD",
        "programs_wm": "PROGRAMS.WM_WD",
        "programs_ref": "PROGRAMS.REF",
    },
    "sensor": {
        "programs_td": "PROGRAMS.TD",
    },
}

NAMES = {
    "switch": {
        "anti_crease": "HDRY_CMD&CTRL.PROGRAM_CYCLE_DETAIL.ANTICREASE_TITLE",
        "add_dish": "DW.ADD_DISH",
        "eco_express": "DW_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.ECO",
        "extra_dry": "DW_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.EXTRA_DRY",
        "half_load": "DW_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.HALF_LOAD",
        "open_door": "DW_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.OPEN_DOOR",
        "three_in_one": "DW_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.THREE_IN_ONE",
        "preheat": "OV.PROGRAM_DETAIL.PREHEAT",
        "dish_washer": "GLOBALS.APPLIANCES_NAME.DW",
        "tumble_dryer": "GLOBALS.APPLIANCES_NAME.TD",
        "washing_machine": "GLOBALS.APPLIANCES_NAME.WM",
        "washer_dryer": "GLOBALS.APPLIANCES_NAME.WD",
        "oven": "GLOBALS.APPLIANCES_NAME.OV",
        "prewash": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.PREWASH",
        "pause": "GENERAL.PAUSE_PROGRAM",
        "keep_fresh": "GLOBALS.APPLIANCE_STATUS.TUMBLING",
        "delay_time": "HINTS.TIPS_TIME_ENERGY_SAVING.TIPS_USE_AT_NIGHT_TITLE",
        "rapid_mode": "AC.PROGRAM_CARD.RAPID",
        "eco_mode": "AC.PROGRAM_CARD.ECO_MODE",
        "10_degree_heating": "PROGRAMS.AC.IOT_10_HEATING",
        "self_clean": "PROGRAMS.AC.IOT_SELF_CLEAN",
        "self_clean_56": "PROGRAMS.AC.IOT_SELF_CLEAN_56",
        "silent_mode": "AC.PROGRAM_DETAIL.SILENT_MODE",
        "mute_mode": "AC.PROGRAM_DETAIL.MUTE_MODE",
        "extra_rinse_1": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.EXTRARINSE1",
        "extra_rinse_2": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.EXTRARINSE2",
        "extra_rinse_3": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.EXTRARINSE3",
        "acqua_plus": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.ACQUAPLUS",
        "auto_dose_softener": [
            "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.AUTODOSE",
            "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.SOFTENER",
        ],
        "auto_dose_detergent": [
            "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.AUTODOSE",
            "WASHING_CMD&CTRL.DASHBOARD_MENU_MORE_SETTINGS_WATER.DETERGENT",
        ],
        "good_night": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.GOODNIGHT",
        "auto_set": "REF_CMD&CTRL.MODALITIES.ECO",
        "super_cool": "REF_CMD&CTRL.MODALITIES.SUPER_COOL",
        "super_freeze": "REF_CMD&CTRL.MODALITIES.SUPER_FREEZE",
    },
    "binary_sensor": {
        "door_lock": "WASHING_CMD&CTRL.CHECK_UP_RESULTS.DOOR_LOCK",
        "extra_rinse_1": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.EXTRARINSE1",
        "extra_rinse_2": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.EXTRARINSE2",
        "extra_rinse_3": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.EXTRARINSE3",
        "good_night": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.GOODNIGHT",
        "anti_crease": "HDRY_CMD&CTRL.PROGRAM_CYCLE_DETAIL.ANTICREASE_TITLE",
        "acqua_plus": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.ACQUAPLUS",
        "spin_speed": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_MAIN_OPTIONS.SPINSPEED",
        "still_hot": "IH.COILS_STATUS.STILL_HOT",
        "pan_status": "IH.COILS_STATUS.PAN",
        "remote_control": "OV.SUPPORT.REMOTE_CONTROL",
        "rinse_aid": "DW_CMD&CTRL.MAINTENANCE.CONSUMABLE_LEVELS_ICON_RINSE_AID",
        "salt_level": "DW_CMD&CTRL.MAINTENANCE.CONSUMABLE_LEVELS_ICON_SALT",
        "door_open": "GLOBALS.APPLIANCE_STATUS.DOOR_OPEN",
        "connection": "ENROLLMENT_COMMON.HEADER_NAME.STEP_APPLIANCE_CONNECTION",
        "child_lock": "AP.FOOTER_MENU_MORE.SECURITY_LOCK_TITLE",
        "on": "GLOBALS.GENERAL.ON",
        "prewash": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OTHER_OPTIONS.PREWASH",
        "buzzer": "DW_CMD&CTRL.SETTINGS.END_CYCLE_BUZZER",
        "holiday_mode": "REF.DASHBOARD_MENU_MORE_NOTIFICATIONS.HOLIDAY_MODE",
        "auto_set": "REF_CMD&CTRL.MODALITIES.ECO",
        "super_cool": "REF_CMD&CTRL.MODALITIES.SUPER_COOL",
        "super_freeze": "REF_CMD&CTRL.MODALITIES.SUPER_FREEZE",
        "freezer_door": ["GLOBALS.APPLIANCE_STATUS.DOOR_OPEN", "REF.ZONES.FREEZER"],
        "fridge_door": ["GLOBALS.APPLIANCE_STATUS.DOOR_OPEN", "REF.ZONES.FRIDGE"],
        "filter_replacement": "AP.MAINTENANCE.FILTER_REPLACEMENT",
    },
    "button": {
        "induction_hob": "GLOBALS.APPLIANCES_NAME.IH",
    },
    "select": {
        "dry_levels": "WASHING_CMD&CTRL.DRAWER_CYCLE_DRYING.TAB_LEVEL",
        "dry_time": "WASHING_CMD&CTRL.DRAWER_CYCLE_DRYING.TAB_TIME",
        "spin_speed": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_MAIN_OPTIONS.SPINSPEED",
        "temperature": "IH.COMMON.TEMPERATURE",
        "programs_dw": "WC.SET_PROGRAM.PROGRAM",
        "programs_ih": "WC.SET_PROGRAM.PROGRAM",
        "programs_ov": "WC.SET_PROGRAM.PROGRAM",
        "programs_td": "WC.SET_PROGRAM.PROGRAM",
        "programs_wm": "WC.SET_PROGRAM.PROGRAM",
        "eco_pilot": "AC.PROGRAM_DETAIL.ECO_PILOT",
        "remaining_time": "ENROLLMENT_COMMON.GENERAL.REMAINING_TIME",
    },
    "sensor": {
        "dry_levels": "WASHING_CMD&CTRL.DRAWER_CYCLE_DRYING.TAB_LEVEL",
        "dry_time": "WASHING_CMD&CTRL.DRAWER_CYCLE_DRYING.TAB_TIME",
        "power": "OV.RECIPE_DETAIL.POWER_LEVEL",
        "remaining_time": "ENROLLMENT_COMMON.GENERAL.REMAINING_TIME",
        "temperature": "IH.COMMON.TEMPERATURE",
        "water_efficiency": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_RESULT.WATER_EFFICIENCY",
        "water_saving": "STATISTICS.SMART_AI_CYCLE.WATER_SAVING",
        "duration": "WASHING_CMD&CTRL.DRAWER_PROGRAM_FILTERS.DURATION",
        "target_temperature": "IH.COOKING_DETAIL.TEMPERATURE_TARGETING",
        "spin_speed": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_MAIN_OPTIONS.SPINSPEED",
        "steam_leve": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_MAIN_OPTIONS.STEAM_LEVEL",
        "dirt_level": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_MAIN_OPTIONS.DIRTY_LEVEL",
        "program_phases_wm": "WASHING_CMD&CTRL.STATISTICS_GRAPHIC_INSTANT_CONSUMPTION.PHASE",
        "program_phases_td": "WASHING_CMD&CTRL.STATISTICS_GRAPHIC_INSTANT_CONSUMPTION.PHASE",
        "program_phases_dw": "WASHING_CMD&CTRL.STATISTICS_GRAPHIC_INSTANT_CONSUMPTION.PHASE",
        "delay_time": "HINTS.TIPS_TIME_ENERGY_SAVING.TIPS_USE_AT_NIGHT_TITLE",
        "suggested_load": "WASHING_CMD&CTRL.DRAWER_PROGRAM_FILTERS.LOAD_CAPACITY",
        "energy_label": "WASHING_CMD&CTRL.DRAWER_PROGRAM_FILTERS.ENERGY_EFFICIENCY",
        "det_dust": "HUBS.WIDGET.STAINS_WIDGET.STAINS.SUGGESTED_DET_DUST",
        "det_liquid": "HUBS.WIDGET.STAINS_WIDGET.STAINS.SUGGESTED_DET_LIQUID",
        "errors": "ROBOT_CMD&CTRL.PHASE_ERROR.TITLE",
        "programs": "OV.TABS.CURRENT_PROGRAM",
        "room_temperature": "REF.SMART_DRINK_ASSISTANT.AMBIENT",
        "humidity": "AP.TITLES.HUMIDITY",
        "cycles_total": [
            "WASHING_CMD&CTRL.GENERAL.CYCLES",
            "WC.VIRTUAL_WINE_STATS_COUNTRY.TOTAL",
        ],
        "energy_total": [
            "MISE.ENERGY_CONSUMPTION.TITLE",
            "WC.VIRTUAL_WINE_STATS_COUNTRY.TOTAL",
        ],
        "water_total": [
            "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_RESULT.WATER_EFFICIENCY",
            "WC.VIRTUAL_WINE_STATS_COUNTRY.TOTAL",
        ],
        "energy_current": [
            "MISE.ENERGY_CONSUMPTION.TITLE",
            "CUBE90_GLOBAL.GENERAL.CURRENT",
        ],
        "water_current": [
            "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_RESULT.WATER_EFFICIENCY",
            "CUBE90_GLOBAL.GENERAL.CURRENT",
        ],
        "freezer_temp": "REF_CMD&CTRL.TEMPERATURE_DRAWER_FREEZER.FREEZER_TEMPERATURE_TITLE",
        "fridge_temp": "REF_CMD&CTRL.TEMPERATURE_DRAWER_FRIDGE.FRIDGE_TEMPERATURE_TITLE",
    },
    "number": {
        "power_management": "HINTS.COOKING_WITH_INDUCTION.POWER_MANAGEMENT",
        "temperature": "IH.COMMON.TEMPERATURE",
        "delay_time": "HINTS.TIPS_TIME_ENERGY_SAVING.TIPS_USE_AT_NIGHT_TITLE",
        "water_hard": "WASHING_CMD&CTRL.DASHBOARD_MENU_MORE_SETTINGS_WATER.TITLE",
        "program_duration": "OV.PROGRAM_DETAIL.PROGRAM_DURATION",
        "target_temperature": "IH.COOKING_DETAIL.TEMPERATURE_TARGETING",
        "rinse_iterations": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL.DRAWER_HEADER_RINSE",
        "wash_time": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL.WASHING_TIME",
        "dry_time": "WASHING_CMD&CTRL.DRAWER_CYCLE_DRYING.TAB_TIME",
        "steam_level": "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_MAIN_OPTIONS.STEAM_LEVEL",
        "freezer_temp_sel": ["OV.COMMON.GOAL_TEMPERATURE", "REF.ZONES.FREEZER"],
        "fridge_temp_sel": ["OV.COMMON.GOAL_TEMPERATURE", "REF.ZONES.FRIDGE"],
    },
    "climate": {"air_conditioner": "GLOBALS.APPLIANCES_NAME.AC"},
}


async def check_translation_files(translations):
    for language in const.LANGUAGES:
        path = translations / f"{language}.json"
        if not path.is_file():
            async with HonAPI(anonymous=True) as hon:
                keys = await hon.translation_keys(language)
                save_json(path, keys)


def load_hon_translations():
    translations = Path(__file__).parent / "translations"
    translations.mkdir(exist_ok=True)
    asyncio.run(check_translation_files(translations))
    return {f.stem: f for f in translations.glob("*.json")}


def load_hass_translations():
    translations = (
        Path(__file__).parent.parent / "custom_components" / "hon" / "translations"
    )
    return {f.stem: f for f in translations.glob("*.json")}


def load_json(path):
    if path:
        with open(path, "r") as file:
            return json.loads(file.read())
    return {}


def save_json(path, keys):
    with open(path, "w") as json_file:
        json_file.write(json.dumps(keys, indent=4, ensure_ascii=False))


def load_key(full_key, json_data, fallback=None):
    if isinstance(full_key, list):
        return " ".join(
            [load_key(item, json_data, fallback).strip() for item in full_key]
        )
    result = json_data.copy()
    for key in full_key.split("."):
        result = result.get(key, {})
    if not result and fallback:
        return load_key(full_key, fallback)
    return result or full_key


def load_keys(full_key, json_data):
    blacklist = ["description", "desctiption", "_recipe_", "_guided_"]
    first, last = full_key.split(".")
    data = json_data.get(first, {}).get(last, {})
    return {
        key.lower(): value
        for key, value in data.items()
        if not any(b in key.lower() for b in blacklist)
        and re.findall("^[a-z0-9-_]+$", key.lower())
    }


def add_data(old, original, fallback, data, name, entity="sensor"):
    sensor = old.setdefault("entity", {}).setdefault(entity, {})
    for number, phase in data.items():
        state = sensor.setdefault(name, {}).setdefault("state", {})
        if key := load_key(phase, original, fallback):
            state[str(number)] = key


def translate_login(old, *args):
    login = old.setdefault("config", {}).setdefault("step", {}).setdefault("user", {})
    login["description"] = load_key("CUBE90_ALEXA.HAIER_SMART_SKILLS.STEP_2", *args)
    login.setdefault("data", {})["email"] = load_key(
        "PET.EDIT_PET_PROFESSIONALS.EMAIL", *args
    )
    login["data"]["password"] = load_key("CUBE90_GLOBAL.GENERAL.PASSWORD", *args)


def main():
    hass = load_hass_translations()
    hon = load_hon_translations()
    base_path = Path(__file__).parent.parent / "custom_components/hon/translations"
    fallback = load_json(hon.get("en", ""))
    for language in const.LANGUAGES:
        original = load_json(hon.get(language, ""))
        old = load_json(hass.get(language, ""))
        for name, data in SENSOR.items():
            add_data(old, original, fallback, data, name)
        for name, data in SELECT.items():
            add_data(old, original, fallback, data, name, "select")
        for entity, data in PROGRAMS.items():
            for name, program in data.items():
                select = old.setdefault("entity", {}).setdefault(entity, {})
                select.setdefault(name, {})["state"] = load_keys(program, original)
        for entity, data in NAMES.items():
            for name, key in data.items():
                select = old.setdefault("entity", {}).setdefault(entity, {})
                select.setdefault(name, {})["name"] = load_key(key, original, fallback)
        translate_login(old, original, fallback)
        save_json(base_path / f"{language}.json", old)


if __name__ == "__main__":
    main()
