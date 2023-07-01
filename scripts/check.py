#!/usr/bin/env python
import sys
from pathlib import Path


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from custom_components.hon.binary_sensor import BINARY_SENSORS
from custom_components.hon.button import BUTTONS
from custom_components.hon.climate import CLIMATES
from custom_components.hon.fan import FANS
from custom_components.hon.light import LIGHTS
from custom_components.hon.lock import LOCKS
from custom_components.hon.number import NUMBERS
from custom_components.hon.select import SELECTS
from custom_components.hon.sensor import SENSORS
from custom_components.hon.switch import SWITCHES

entities = {
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


def get_missing_translation_keys():
    result = {}
    for entity_type, appliances in entities.items():
        for appliance, data in appliances.items():
            for entity in data:
                if entity.translation_key:
                    continue
                key = f"{entity_type}.{entity.key}"
                result.setdefault(appliance, []).append(key)
    return result


if __name__ == "__main__":
    for appliance, data in sorted(get_missing_translation_keys().items()):
        for key in data:
            print(f"WARNING - {appliance} - Missing translation key for {key}")
