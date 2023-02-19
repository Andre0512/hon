from pyhon.device import HonDevice

from .const import DOMAIN
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity


class HonEntity(CoordinatorEntity):
    _attr_has_entity_name = True

    def __init__(self, hass, entry, coordinator, device: HonDevice) -> None:
        super().__init__(coordinator)

        self._hon = hass.data[DOMAIN][entry.unique_id]
        self._hass = hass
        self._device = device

        self._attr_unique_id = self._device.mac_address

    @property
    def device_info(self):
        """Return a device description for device registry."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device.mac_address)},
            manufacturer=self._device.brand,
            name=self._device.nick_name if self._device.nick_name else self._device.model_name,
            model=self._device.model_name,
            sw_version=self._device.fw_version,
        )
