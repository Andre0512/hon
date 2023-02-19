import logging
from datetime import timedelta

import voluptuous as vol
from pyhon import HonConnection
from pyhon.device import HonDevice

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.helpers import config_validation as cv, aiohttp_client
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from custom_components.hon.const import DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)


HON_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_EMAIL): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.Schema(vol.All(cv.ensure_list, [HON_SCHEMA]))},
    extra=vol.ALLOW_EXTRA,
)


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    session = aiohttp_client.async_get_clientsession(hass)
    hon = HonConnection(entry.data["email"], entry.data["password"], session)
    await hon.setup()
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.unique_id] = hon
    hass.data[DOMAIN]["coordinators"] = {}

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )


class HonCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, device: HonDevice):
        """Initialize my coordinator."""
        super().__init__(hass, _LOGGER, name=device.mac_address, update_interval=timedelta(seconds=30))
        self._device = device

    async def _async_update_data(self):
        await self._device.load_attributes()
