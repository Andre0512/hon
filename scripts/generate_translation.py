#!/usr/bin/env python

import asyncio
import json
import re
from pathlib import Path

from pyhon import HonAPI

# These languages are official supported by hOn
LANGUAGES = [
    "cs",  # Czech
    "de",  # German
    "el",  # Greek
    "en",  # English
    "es",  # Spanish
    "fr",  # French
    "he",  # Hebrew
    "hr",  # Croatian
    "it",  # Italian
    "nl",  # Dutch
    "pl",  # Polish
    "pt",  # Portuguese
    "ro",  # Romanian
    "ru",  # Russian
    "sk",  # Slovak
    "sl",  # Slovenian
    "sr",  # Serbian
    "tr",  # Turkish
    "zh",  # Chinese
]

WASHING_PR_PHASE = {
    0: "WASHING_CMD&CTRL.PHASE_READY.TITLE",
    1: "WASHING_CMD&CTRL.PHASE_WASHING.TITLE",
    2: "WASHING_CMD&CTRL.PHASE_WASHING.TITLE",
    3: "WASHING_CMD&CTRL.PHASE_SPIN.TITLE",
    4: "WASHING_CMD&CTRL.PHASE_RINSE.TITLE",
    5: "WASHING_CMD&CTRL.PHASE_RINSE.TITLE",
    6: "WASHING_CMD&CTRL.PHASE_RINSE.TITLE",
    7: "WASHING_CMD&CTRL.PHASE_DRYING.TITLE",
    9: "WASHING_CMD&CTRL.PHASE_STEAM.TITLE",
    10: "WASHING_CMD&CTRL.PHASE_READY.TITLE",
    11: "WASHING_CMD&CTRL.PHASE_SPIN.TITLE",
    12: "WASHING_CMD&CTRL.PHASE_WEIGHTING.TITLE",
    13: "WASHING_CMD&CTRL.PHASE_WEIGHTING.TITLE",
    14: "WASHING_CMD&CTRL.PHASE_WASHING.TITLE",
    15: "WASHING_CMD&CTRL.PHASE_WASHING.TITLE",
    16: "WASHING_CMD&CTRL.PHASE_WASHING.TITLE",
    17: "WASHING_CMD&CTRL.PHASE_RINSE.TITLE",
    18: "WASHING_CMD&CTRL.PHASE_RINSE.TITLE",
    19: "WASHING_CMD&CTRL.PHASE_SCHEDULED.TITLE",
    20: "WASHING_CMD&CTRL.PHASE_TUMBLING.TITLE",
    24: "WASHING_CMD&CTRL.PHASE_REFRESH.TITLE",
    25: "WASHING_CMD&CTRL.PHASE_WASHING.TITLE",
    26: "WASHING_CMD&CTRL.PHASE_HEATING.TITLE",
    27: "WASHING_CMD&CTRL.PHASE_WASHING.TITLE",
}
MACH_MODE = {
    0: "WASHING_CMD&CTRL.PHASE_READY.TITLE",
    1: "WASHING_CMD&CTRL.PHASE_READY.TITLE",
    3: "WASHING_CMD&CTRL.PHASE_PAUSE.TITLE",
    4: "WASHING_CMD&CTRL.PHASE_SCHEDULED.TITLE",
    5: "WASHING_CMD&CTRL.PHASE_SCHEDULED.TITLE",
    6: "WASHING_CMD&CTRL.PHASE_ERROR.TITLE",
    7: "WASHING_CMD&CTRL.PHASE_READY.TITLE",
}
TUMBLE_DRYER_PR_PHASE = {
    0: "WASHING_CMD&CTRL.PHASE_READY.TITLE",
    1: "TD_CMD&CTRL.STATUS_PHASE.PHASE_HEAT_STROKE",
    2: "WASHING_CMD&CTRL.PHASE_DRYING.TITLE",
    3: "TD_CMD&CTRL.STATUS_PHASE.PHASE_COOLDOWN",
    13: "TD_CMD&CTRL.STATUS_PHASE.PHASE_COOLDOWN",
    14: "TD_CMD&CTRL.STATUS_PHASE.PHASE_HEAT_STROKE",
    15: "TD_CMD&CTRL.STATUS_PHASE.PHASE_HEAT_STROKE",
    16: "TD_CMD&CTRL.STATUS_PHASE.PHASE_COOLDOWN",
    18: "WASHING_CMD&CTRL.PHASE_TUMBLING.DASHBOARD_TITLE",
    19: "WASHING_CMD&CTRL.PHASE_DRYING.TITLE",
    20: "WASHING_CMD&CTRL.PHASE_DRYING.TITLE",
}
DISHWASHER_PR_PHASE = {
    0: "WASHING_CMD&CTRL.PHASE_READY.TITLE",
    1: "WASHING_CMD&CTRL.PHASE_PREWASH.TITLE",
    2: "WASHING_CMD&CTRL.PHASE_WASHING.TITLE",
    3: "WASHING_CMD&CTRL.PHASE_RINSE.TITLE",
    4: "WASHING_CMD&CTRL.PHASE_DRYING.TITLE",
    5: "WASHING_CMD&CTRL.PHASE_READY.TITLE",
    6: "WASHING_CMD&CTRL.PHASE_HOT_RINSE.TITLE",
}

TUMBLE_DRYER_DRY_LEVEL = {
    0: "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_MAIN_OPTIONS.NO_DRY",
    1: "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OPTIONS_VALUES_DESCRIPTION.IRON_DRY",
    2: "WASHING_CMD&CTRL.GUIDED_WASHING_SYMBOLS_DRYING.NO_DRY_IRON_TITLE",
    3: "WASHING_CMD&CTRL.GUIDED_WASHING_SYMBOLS_DRYING.CUPBOARD_DRY_TITLE",
    4: "WASHING_CMD&CTRL.GUIDED_WASHING_SYMBOLS_DRYING.EXTRA_DRY_TITLE",
    12: "WASHING_CMD&CTRL.PROGRAM_CYCLE_DETAIL_OPTIONS_VALUES_DESCRIPTION.IRON_DRY",
    13: "WASHING_CMD&CTRL.GUIDED_WASHING_SYMBOLS_DRYING.CUPBOARD_DRY_TITLE",
    14: "WASHING_CMD&CTRL.GUIDED_WASHING_SYMBOLS_DRYING.READY_TO_WEAR_TITLE",
    15: "WASHING_CMD&CTRL.GUIDED_WASHING_SYMBOLS_DRYING.EXTRA_DRY_TITLE",
}

SENSOR = {
    "washing_modes": MACH_MODE,
    "program_phases_wm": WASHING_PR_PHASE,
    "program_phases_td": TUMBLE_DRYER_PR_PHASE,
    "program_phases_dw": DISHWASHER_PR_PHASE,
    "dry_levels": TUMBLE_DRYER_DRY_LEVEL,
}

SELECT = {"dry_levels": TUMBLE_DRYER_DRY_LEVEL}

PROGRAMS = {
    "programs_dw": "PROGRAMS.DW",
    "programs_ih": "PROGRAMS.IH",
    "programs_ov": "PROGRAMS.OV",
    "programs_td": "PROGRAMS.TD",
    "programs_wm": "PROGRAMS.WM_WD",
}


async def check_translation_files(translations):
    for language in LANGUAGES:
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
        json_file.write(json.dumps(keys, indent=4))


def load_key(full_key, json_data, fallback=None):
    result = json_data.copy()
    for key in full_key.split("."):
        result = result.get(key, {})
    if not result and fallback:
        return load_key(full_key, fallback)
    return result or ""


def load_keys(full_key, json_data):
    blacklist = ["description", "_recipe_", "_guided_"]
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


def main():
    hass = load_hass_translations()
    hon = load_hon_translations()
    base_path = Path(__file__).parent.parent / "custom_components/hon/translations"
    fallback = load_json(hon.get("en", ""))
    for language in LANGUAGES:
        original = load_json(hon.get(language, ""))
        old = load_json(hass.get(language, ""))
        for name, data in SENSOR.items():
            add_data(old, original, fallback, data, name)
        for name, data in SELECT.items():
            add_data(old, original, fallback, data, name, "select")
        for name, program in PROGRAMS.items():
            select = old.setdefault("entity", {}).setdefault("select", {})
            select.setdefault(name, {})["state"] = load_keys(program, original)
        save_json(base_path / f"{language}.json", old)


if __name__ == "__main__":
    main()
