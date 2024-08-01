import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

class ConnectLifeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # Validate user input here if necessary
            return self.async_create_entry(title="ConnectLife", data=user_input)

        data_schema = vol.Schema({
            vol.Required("puid"): str,
            vol.Required("device_id"): str,
            vol.Required("update_frequency"): vol.Coerce(int),
            vol.Required("homeassistant_host"): str,
            vol.Required("port"): str
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return ConnectLifeOptionsFlow(config_entry)

class ConnectLifeOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema({
            vol.Optional("puid", default=self.config_entry.data.get("puid")): str,
            vol.Optional("device_id", default=self.config_entry.data.get("device_id")): str,
            vol.Optional("update_frequency", default=self.config_entry.data.get("update_frequency")): vol.Coerce(int),
            vol.Optional("homeassistant_host", default=self.config_entry.data.get("homeassistant_host")): str,
            vol.Optional("port", default=self.config_entry.data.get("port")): str
        })

        return self.async_show_form(step_id="user", data_schema=data_schema)