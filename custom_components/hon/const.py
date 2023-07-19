from homeassistant.components.climate import (
    HVACMode,
    FAN_LOW,
    FAN_MEDIUM,
    FAN_HIGH,
    FAN_AUTO,
)

DOMAIN = "hon"
UPDATE_INTERVAL = 10

PLATFORMS = [
    "sensor",
    "select",
    "number",
    "switch",
    "button",
    "binary_sensor",
    "climate",
    "fan",
    "light",
    "lock",
]

APPLIANCES = {
    "AC": "Air Conditioner",
    "AP": "Air Purifier",
    "AS": "Air Scanner",
    "DW": "Dish Washer",
    "HO": "Hood",
    "IH": "Induction Hob",
    "MW": "Microwave",
    "OV": "Oven",
    "REF": "Fridge",
    "RVC": "Robot Vacuum Cleaner",
    "TD": "Tumble Dryer",
    "WC": "Wine Cellar",
    "WD": "Washer Dryer",
    "WH": "Water Heater",
    "WM": "Washing Machine",
}

HON_HVAC_MODE = {
    0: HVACMode.AUTO,
    1: HVACMode.COOL,
    2: HVACMode.DRY,
    3: HVACMode.DRY,
    4: HVACMode.HEAT,
    5: HVACMode.FAN_ONLY,
    6: HVACMode.FAN_ONLY,
}

HON_HVAC_PROGRAM = {
    HVACMode.AUTO: "iot_auto",
    HVACMode.COOL: "iot_cool",
    HVACMode.DRY: "iot_dry",
    HVACMode.HEAT: "iot_heat",
    HVACMode.FAN_ONLY: "iot_fan",
}

HON_FAN = {
    1: FAN_HIGH,
    2: FAN_MEDIUM,
    3: FAN_LOW,
    4: FAN_AUTO,
    5: FAN_AUTO,
}

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
    0: "ready",
    1: "washing",
    2: "washing",
    3: "spin",
    4: "rinse",
    5: "rinse",
    6: "rinse",
    7: "drying",
    9: "steam",
    10: "ready",
    11: "spin",
    12: "weighting",
    13: "weighting",
    14: "washing",
    15: "washing",
    16: "washing",
    17: "rinse",
    18: "rinse",
    19: "scheduled",
    20: "tumbling",
    24: "refresh",
    25: "washing",
    26: "heating",
    27: "washing",
}

MACH_MODE = {
    0: "ready",  # NO_STATE
    1: "ready",  # SELECTION_MODE
    2: "running",  # EXECUTION_MODE
    3: "pause",  # PAUSE_MODE
    4: "scheduled",  # DELAY_START_SELECTION_MODE
    5: "scheduled",  # DELAY_START_EXECUTION_MODE
    6: "error",  # ERROR_MODE
    7: "ready",  # END_MODE
    8: "test",  # TEST_MODE
    9: "ending",  # STOP_MODE
}

TUMBLE_DRYER_PR_PHASE = {
    0: "ready",
    1: "heat_stroke",
    2: "drying",
    3: "cooldown",
    8: "unknown",
    11: "ready",
    12: "unknown",
    13: "cooldown",
    14: "heat_stroke",
    15: "heat_stroke",
    16: "cooldown",
    17: "unknown",
    18: "tumbling",
    19: "drying",
    20: "drying",
}

DIRTY_LEVEL = {
    0: "unknown",
    1: "little",
    2: "normal",
    3: "very",
}

STEAM_LEVEL = {
    0: "no_steam",
    1: "cotton",
    2: "delicate",
    3: "synthetic",
}

DISHWASHER_PR_PHASE = {
    0: "ready",
    1: "prewash",
    2: "washing",
    3: "rinse",
    4: "drying",
    5: "ready",
    6: "hot_rinse",
}

TUMBLE_DRYER_DRY_LEVEL = {
    0: "no_dry",
    1: "iron_dry",
    2: "no_dry_iron",
    3: "cupboard_dry",
    4: "extra_dry",
    11: "no_dry",
    12: "iron_dry",
    13: "cupboard_dry",
    14: "ready_to_wear",
    15: "extra_dry",
}

AC_MACH_MODE = {
    0: "auto",
    1: "cool",
    2: "cool",
    3: "dry",
    4: "heat",
    5: "fan",
    6: "fan",
}

AC_FAN_MODE = {
    1: "high",
    2: "mid",
    3: "low",
    4: "auto",
    5: "auto",
}

AC_HUMAN_SENSE = {
    0: "touch_off",
    1: "avoid_touch",
    2: "follow_touch",
    3: "unknown",
}

AP_MACH_MODE = {
    0: "standby",
    1: "sleep",
    2: "auto",
    3: "allergens",
    4: "max",
}

AP_DIFFUSER_LEVEL = {
    0: "off",
    1: "soft",
    2: "mid",
    3: "h_biotics",
    4: "custom",
}

REF_HUMIDITY_LEVELS = {1: "low", 2: "mid", 3: "high"}
