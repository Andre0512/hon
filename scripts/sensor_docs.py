from custom_components.hon.binary_sensor import BINARY_SENSORS
from custom_components.hon.button import BUTTONS
from custom_components.hon.number import NUMBERS
from custom_components.hon.select import SELECTS
from custom_components.hon.sensor import SENSORS
from custom_components.hon.switch import SWITCHES

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
}

result = {}
for entity_type, appliances in entities.items():
    for appliance, data in appliances.items():
        for entity in data:
            attributes = (entity.key, entity.name, entity.icon, entity_type)
            category = "control" if entity_type in ["switch", "button"] else "sensor"
            result.setdefault(appliance, {}).setdefault(
                entity.entity_category or category, []
            ).append(attributes)

for appliance, categories in sorted(result.items()):
    print(f"### {APPLIANCES[appliance]}")
    categories = {k: categories[k] for k in ENTITY_CATEGORY_SORT if k in categories}
    for category, data in categories.items():
        print(f"#### {str(category).capitalize()}s")
        print("| Name | Icon | Entity | Key |")
        print("| --- | --- | --- | --- |")
        for key, name, icon, entity_type in sorted(data, key=lambda d: d[1]):
            icon = f"`{icon}`" if icon else ""
            print(f"| {name} | {icon} | `{entity_type}` | `{key}` |")
