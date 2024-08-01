import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

@config_entries.HANDLERS.register(DOMAIN)
class ConnectLifeClimateFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="ConnectLife Climate", data=user_input)

        data_schema = vol.Schema({
            vol.Required("api_url"): str,
            vol.Required("device_id"): str,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return ConnectLifeClimateOptionsFlowHandler(config_entry)

class ConnectLifeClimateOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema({
            vol.Required("api_url", default=self.config_entry.data.get("api_url")): str,
            vol.Required("device_id", default=self.config_entry.data.get("device_id")): str,
        })

        return self.async_show_form(step_id="init", data_schema=data_schema, errors=errors)