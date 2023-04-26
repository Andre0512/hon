from homeassistant.components.climate import HVACMode

from custom_components.hon import climate

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
    "1": climate.FAN_HIGH,
    "2": climate.FAN_MEDIUM,
    "3": climate.FAN_LOW,
    "4": climate.FAN_AUTO,
    "5": climate.FAN_AUTO,
}
