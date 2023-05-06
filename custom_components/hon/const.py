from homeassistant.components.climate import (
    HVACMode,
    FAN_LOW,
    FAN_MEDIUM,
    FAN_HIGH,
    FAN_AUTO,
)

DOMAIN = "hon"

PLATFORMS = [
    "sensor",
    "select",
    "number",
    "switch",
    "button",
    "binary_sensor",
    "climate",
]

HON_HVAC_MODE = {
    "0": HVACMode.AUTO,
    "1": HVACMode.COOL,
    "2": HVACMode.COOL,
    "3": HVACMode.DRY,
    "4": HVACMode.HEAT,
    "5": HVACMode.FAN_ONLY,
    "6": HVACMode.FAN_ONLY,
}

HON_HVAC_PROGRAM = {
    HVACMode.AUTO: "iot_auto",
    HVACMode.COOL: "iot_cool",
    HVACMode.DRY: "iot_dry",
    HVACMode.HEAT: "iot_heat",
    HVACMode.FAN_ONLY: "iot_fan",
}

HON_FAN = {
    "1": FAN_HIGH,
    "2": FAN_MEDIUM,
    "3": FAN_LOW,
    "4": FAN_AUTO,
    "5": FAN_AUTO,
}
