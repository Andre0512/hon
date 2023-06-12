import logging
from contextlib import suppress
from datetime import timedelta

from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pyhon.appliance import HonAppliance

from .const import DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class HonEntity(CoordinatorEntity):
    _attr_has_entity_name = True

    def __init__(self, hass, entry, device: HonAppliance, description=None) -> None:
        coordinator = get_coordinator(hass, device)
        super().__init__(coordinator)

        self._hon = hass.data[DOMAIN][entry.unique_id]
        self._hass = hass
        self._coordinator = coordinator
        self._device: HonAppliance = device

        if description is not None:
            self.entity_description = description
            self._attr_unique_id = f"{self._device.unique_id}{description.key}"
        else:
            self._attr_unique_id = self._device.unique_id
        self._handle_coordinator_update(update=False)

    @property
    def device_info(self):
        return DeviceInfo(
            identifiers={(DOMAIN, self._device.unique_id)},
            manufacturer=self._device.get("brand", ""),
            name=self._device.nick_name
            if self._device.nick_name
            else self._device.model_name,
            model=self._device.model_name,
            sw_version=self._device.get("fwVersion", ""),
        )

    @callback
    def _handle_coordinator_update(self, update: bool = True) -> None:
        if update:
            self.async_write_ha_state()


class HonCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, device: HonAppliance):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=device.unique_id,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )
        self._device = device

    async def _async_update_data(self):
        await self._device.update()


def unique_entities(base_entities, new_entities):
    result = list(base_entities)
    existing_entities = [entity.key for entity in base_entities]
    for entity in new_entities:
        if entity.key not in existing_entities:
            result.append(entity)
    return tuple(result)


def get_coordinator(hass, appliance):
    coordinators = hass.data[DOMAIN]["coordinators"]
    if appliance.unique_id in coordinators:
        coordinator = hass.data[DOMAIN]["coordinators"][appliance.unique_id]
    else:
        coordinator = HonCoordinator(hass, appliance)
        hass.data[DOMAIN]["coordinators"][appliance.unique_id] = coordinator
    return coordinator


def get_readable(description, value):
    with suppress(ValueError):
        return description.option_list.get(int(value), value)
