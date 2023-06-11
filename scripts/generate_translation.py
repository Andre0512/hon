#!/usr/bin/env python

import asyncio
import json
import re
import sys
from pathlib import Path

from pyhon import HonAPI


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.translation_keys import SENSOR, SELECT, PROGRAMS, NAMES, CLIMATE
from custom_components.hon import const


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
        for name, modes in CLIMATE.items():
            climate = old.setdefault("entity", {}).setdefault("climate", {})
            attr = climate.setdefault(name, {}).setdefault("state_attributes", {})
            for mode, data in modes.items():
                mode_name = load_key(data["name"], original, fallback)
                attr.setdefault(mode, {})["name"] = mode_name
                if isinstance(data["state"], dict):
                    for state, key in data["state"].items():
                        mode_state = load_key(key, original, fallback)
                        attr[mode].setdefault("state", {})[state] = mode_state
                else:
                    attr[mode]["state"] = load_keys(data["state"], original)

        translate_login(old, original, fallback)
        save_json(base_path / f"{language}.json", old)


if __name__ == "__main__":
    main()
