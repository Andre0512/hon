import logging
from pathlib import Path

import voluptuous as vol  # type: ignore[import]
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.helpers import config_validation as cv, aiohttp_client
from homeassistant.helpers.typing import HomeAssistantType
from pyhon import Hon

from .const import DOMAIN, PLATFORMS

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


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry) -> bool:
    session = aiohttp_client.async_get_clientsession(hass)
    if (config_dir := hass.config.config_dir) is None:
        raise ValueError("Missing Config Dir")
    hon = await Hon(
        entry.data["email"],
        entry.data["password"],
        session=session,
        test_data_path=Path(config_dir),
    ).create()
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.unique_id] = hon
    hass.data[DOMAIN]["coordinators"] = {}

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )
    return True


async def async_unload_entry(hass: HomeAssistantType, entry: ConfigEntry) -> bool:
    unload = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload:
        if not hass.data[DOMAIN]:
            hass.data.pop(DOMAIN, None)
    return unload
