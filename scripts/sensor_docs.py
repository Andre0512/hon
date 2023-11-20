#!/usr/bin/env python

import re
import sys
from pathlib import Path

from homeassistant.util import yaml

if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from custom_components.hon.const import APPLIANCES
from custom_components.hon.binary_sensor import BINARY_SENSORS
from custom_components.hon.button import BUTTONS
from custom_components.hon.climate import CLIMATES
from custom_components.hon.fan import FANS
from custom_components.hon.light import LIGHTS
from custom_components.hon.lock import LOCKS
from custom_components.hon.number import NUMBERS
from custom_components.hon.select import SELECTS
from custom_components.hon.sensor import SENSORS
from custom_components.hon.switch import (
    SWITCHES,
    HonControlSwitchEntityDescription,
    HonSwitchEntityDescription,
)

ENTITY_CATEGORY_SORT = ["control", "config", "sensor"]

ENTITIES = {
    "binary_sensor": BINARY_SENSORS,
    "button": BUTTONS,
    "climate": CLIMATES,
    "fan": FANS,
    "light": LIGHTS,
    "lock": LOCKS,
    "number": NUMBERS,
    "select": SELECTS,
    "sensor": SENSORS,
    "switch": SWITCHES,
}


def get_models():
    return yaml.load_yaml(str(Path(__file__).parent.parent / "supported_models.yml"))


def get_entites():
    result = {}
    for entity_type, appliances in ENTITIES.items():
        for appliance, data in appliances.items():
            for entity in data:
                if isinstance(entity, HonControlSwitchEntityDescription):
                    key = f"{entity.turn_on_key}` / `{entity.turn_off_key}"
                else:
                    key = entity.key
                attributes = (key, entity.name, entity.icon, entity_type)
                category = (
                    "control"
                    if entity.key.startswith("settings")
                    or isinstance(entity, HonSwitchEntityDescription)
                    or isinstance(entity, HonControlSwitchEntityDescription)
                    or entity_type in ["button", "climate", "lock", "light", "fan"]
                    else "sensor"
                )
                result.setdefault(appliance, {}).setdefault(
                    entity.entity_category or category, []
                ).append(attributes)
    return result


def generate_text(entites, models):
    text = "_Click to expand..._\n\n"
    for appliance, categories in sorted(entites.items()):
        text += f"<details>\n<summary>{APPLIANCES[appliance]}</summary>\n\n"
        example = f"example_{appliance.lower()}.png"
        if (Path(__file__).parent.parent / "assets" / example).exists():
            text += f"### {APPLIANCES[appliance]} Example\n![{APPLIANCES[appliance]}](assets/{example})\n\n"
        support_number = sum([len(e) for e in models[appliance.lower()].values()])
        text += (
            f"### Supported {APPLIANCES[appliance]} models\nSupport has been confirmed for these "
            f"**{support_number} models**, but many more will work. Please add already supported devices "
            f"[with this form to complete the list](https://forms.gle/bTSD8qFotdZFytbf8).\n"
        )
        for brand, items in models[appliance.lower()].items():
            text += f"\n#### {brand[0].upper()}{brand[1:]}\n- "
            text += "\n- ".join(items) + "\n"
        categories = {k: categories[k] for k in ENTITY_CATEGORY_SORT if k in categories}
        text += f"\n### {APPLIANCES[appliance]} Entities\n"
        for category, data in categories.items():
            text += f"#### {str(category).capitalize()}s\n"
            text += "| Name | Icon | Entity | Key |\n"
            text += "| --- | --- | --- | --- |\n"
            for key, name, icon, entity_type in sorted(data, key=lambda d: d[1]):
                icon = f"`{icon.replace('mdi:', '')}`" if icon else ""
                text += f"| {name} | {icon} | `{entity_type}` | `{key}` |\n"
        text += "\n</details>\n\n"
    return text


def update_readme(text, entities, models, file_name="README.md"):
    with open(Path(__file__).parent.parent / file_name, "r") as file:
        readme = file.read()
    readme = re.sub(
        "(## Supported Appliances\n)(?:.|\\s)+?([^#]## |\\Z)",
        f"\\1{text}\\2",
        readme,
        re.DOTALL,
    )
    entities = sum(len(x) for cat in entities.values() for x in cat.values())
    readme = re.sub("badge/Entities-\\d+", f"badge/Entities-{entities}", readme)
    models = sum(len(x) for cat in models.values() for x in cat.values())
    readme = re.sub("badge/Models-\\d+", f"badge/Models-{models}", readme)
    with open(Path(__file__).parent.parent / file_name, "w") as file:
        file.write(readme)


if __name__ == "__main__":
    entities = get_entites()
    models = get_models()
    text = generate_text(entities, models)
    update_readme(text, entities, models)
    update_readme(text, entities, models, "info.md")
