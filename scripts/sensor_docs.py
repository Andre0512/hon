#!/usr/bin/env python

import re
import sys
from pathlib import Path


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from custom_components.hon.binary_sensor import BINARY_SENSORS
from custom_components.hon.button import BUTTONS
from custom_components.hon.climate import CLIMATES
from custom_components.hon.number import NUMBERS
from custom_components.hon.select import SELECTS
from custom_components.hon.sensor import SENSORS
from custom_components.hon.switch import SWITCHES, HonSwitchEntityDescription

APPLIANCES = {
    "AC": "Air conditioner",
    "AP": "Air purifier",
    "AS": "Air scanner",
    "DW": "Dish washer",
    "HO": "Hood",
    "IH": "Hob",
    "MW": "Microwave",
    "OV": "Oven",
    "REF": "Fridge",
    "RVC": "Robot vacuum cleaner",
    "TD": "Tumble dryer",
    "WC": "Wine Cellar",
    "WD": "Washer dryer",
    "WH": "Water Heater",
    "WM": "Washing machine",
}

ENTITY_CATEGORY_SORT = ["control", "config", "sensor"]

entities = {
    "binary_sensor": BINARY_SENSORS,
    "button": BUTTONS,
    "number": NUMBERS,
    "select": SELECTS,
    "sensor": SENSORS,
    "switch": SWITCHES,
    "climate": CLIMATES,
}

result = {}
for entity_type, appliances in entities.items():
    for appliance, data in appliances.items():
        for entity in data:
            if (
                isinstance(entity, HonSwitchEntityDescription)
                and entity.entity_category != "config"
                and "settings." not in entity.key
            ):
                key = f"{entity.turn_on_key}` / `{entity.turn_off_key}"
            else:
                key = entity.key
            attributes = (key, entity.name, entity.icon, entity_type)
            category = (
                "control"
                if entity.key.startswith("settings")
                or hasattr(entity, "turn_on_key")
                or entity_type in ["button", "climate"]
                else "sensor"
            )
            result.setdefault(appliance, {}).setdefault(
                entity.entity_category or category, []
            ).append(attributes)
text = ""
for appliance, categories in sorted(result.items()):
    text += f"\n### {APPLIANCES[appliance]}\n"
    categories = {k: categories[k] for k in ENTITY_CATEGORY_SORT if k in categories}
    for category, data in categories.items():
        text += f"#### {str(category).capitalize()}s\n"
        text += "| Name | Icon | Entity | Key |\n"
        text += "| --- | --- | --- | --- |\n"
        for key, name, icon, entity_type in sorted(data, key=lambda d: d[1]):
            icon = f"`{icon.replace('mdi:', '')}`" if icon else ""
            text += f"| {name} | {icon} | `{entity_type}` | `{key}` |\n"

with open(Path(__file__).parent.parent / "README.md", "r") as file:
    readme = file.read()
readme = re.sub(
    "(## Appliance Features\n)(?:.|\\s)+?([^#]## |\\Z)",
    f"\\1{text}\\2",
    readme,
    re.DOTALL,
)
with open(Path(__file__).parent.parent / "README.md", "w") as file:
    file.write(readme)
