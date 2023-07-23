from typing import Union, TypeVar

from homeassistant.components.button import ButtonEntityDescription
from homeassistant.components.fan import FanEntityDescription
from homeassistant.components.light import LightEntityDescription
from homeassistant.components.lock import LockEntityDescription
from homeassistant.components.number import NumberEntityDescription
from homeassistant.components.select import SelectEntityDescription
from homeassistant.components.sensor import SensorEntityDescription
from homeassistant.components.switch import SwitchEntityDescription

from .binary_sensor import HonBinarySensorEntityDescription
from .button import HonButtonEntity, HonDataArchive, HonDeviceInfo
from .climate import (
    HonACClimateEntityDescription,
    HonClimateEntityDescription,
)
from .number import (
    HonConfigNumberEntityDescription,
    HonNumberEntityDescription,
)
from .select import (
    HonConfigSelectEntityDescription,
    HonSelectEntityDescription,
)
from .sensor import (
    HonSensorEntityDescription,
    HonConfigSensorEntityDescription,
)
from .switch import (
    HonControlSwitchEntityDescription,
    HonSwitchEntityDescription,
    HonConfigSwitchEntityDescription,
)

HonButtonType = Union[
    HonButtonEntity,
    HonDataArchive,
    HonDeviceInfo,
]

HonEntityDescription = Union[
    HonBinarySensorEntityDescription,
    HonControlSwitchEntityDescription,
    HonSwitchEntityDescription,
    HonConfigSwitchEntityDescription,
    HonSensorEntityDescription,
    HonConfigSelectEntityDescription,
    HonConfigNumberEntityDescription,
    HonACClimateEntityDescription,
    HonClimateEntityDescription,
    HonNumberEntityDescription,
    HonSelectEntityDescription,
    HonConfigSensorEntityDescription,
    FanEntityDescription,
    LightEntityDescription,
    LockEntityDescription,
    ButtonEntityDescription,
    SwitchEntityDescription,
    SensorEntityDescription,
    SelectEntityDescription,
    NumberEntityDescription,
]

HonOptionEntityDescription = Union[
    HonConfigSelectEntityDescription,
    HonSelectEntityDescription,
    HonConfigSensorEntityDescription,
    HonSensorEntityDescription,
]

T = TypeVar(
    "T",
    HonBinarySensorEntityDescription,
    HonControlSwitchEntityDescription,
    HonSwitchEntityDescription,
    HonConfigSwitchEntityDescription,
    HonSensorEntityDescription,
    HonConfigSelectEntityDescription,
    HonConfigNumberEntityDescription,
    HonACClimateEntityDescription,
    HonClimateEntityDescription,
    HonNumberEntityDescription,
    HonSelectEntityDescription,
    HonConfigSensorEntityDescription,
    FanEntityDescription,
    LightEntityDescription,
    LockEntityDescription,
    ButtonEntityDescription,
    SwitchEntityDescription,
    SensorEntityDescription,
    SelectEntityDescription,
    NumberEntityDescription,
)
