import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class HonFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        self._email = None
        self._password = None

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {vol.Required(CONF_EMAIL): str, vol.Required(CONF_PASSWORD): str}
                ),
            )

        self._email = user_input[CONF_EMAIL]
        self._password = user_input[CONF_PASSWORD]

        # Check if already configured
        await self.async_set_unique_id(self._email)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=self._email,
            data={
                CONF_EMAIL: self._email,
                CONF_PASSWORD: self._password,
            },
        )

    async def async_step_import(self, user_input=None):
        return await self.async_step_user(user_input)
