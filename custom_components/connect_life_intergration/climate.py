import logging
import requests
import aiohttp
import json
import datetime
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    HVAC_MODE_HEAT,
    HVAC_MODE_COOL,
    HVAC_MODE_AUTO,
    HVAC_MODE_DRY,
    HVAC_MODE_FAN_ONLY,
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_FAN_MODE,
    SUPPORT_SWING_MODE,
    SWING_OFF,
    SWING_ON,
    FAN_AUTO,
    FAN_LOW,
    FAN_MEDIUM,
    FAN_MIDDLE,
    FAN_HIGH
)
from homeassistant.const import TEMP_CELSIUS, ATTR_TEMPERATURE
from homeassistant.helpers.event import async_track_time_interval
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config, async_add_entities, discovery_info=None):
    api_url = config.get("api_url")
    device_id = config.get("device_id")
    climate_entity = ConnectLifeClimate(api_url, device_id)
    async_add_entities([climate_entity])
    async_track_time_interval(hass, climate_entity.async_update, datetime.timedelta(minutes=1))

class ConnectLifeClimate(ClimateEntity):
    def __init__(self, api_url, device_id):
        self._recently_updated = False
        self._name = "ConnectLife Climate"
        self._temperature = 26.0
        self._target_temperature = 23.0
        self._hvac_mode = HVAC_MODE_COOL
        self._fan_mode = "auto"
        self._swing_mode = "off"
        self._api_url = api_url
        self._device_id = device_id
        self._attr_hvac_modes = [
            HVAC_MODE_AUTO,
            HVAC_MODE_HEAT,
            HVAC_MODE_COOL,
            HVAC_MODE_DRY,
            HVAC_MODE_FAN_ONLY
        ]
        self._attr_fan_modes = [
            FAN_AUTO,
            FAN_LOW,
            FAN_MEDIUM,
            FAN_MIDDLE,
            FAN_HIGH
        ]
        self._attr_swing_modes = [
            SWING_OFF,
            SWING_ON
        ]

    @property
    def name(self):
        return self._name

    @property
    def temperature_unit(self):
        return TEMP_CELSIUS

    @property
    def hvac_mode(self):
        return self._hvac_mode

    @property
    def current_temperature(self):
        return self._temperature

    @property
    def target_temperature(self):
        return self._target_temperature

    @property
    def supported_features(self):
        return SUPPORT_TARGET_TEMPERATURE | SUPPORT_FAN_MODE | SUPPORT_SWING_MODE

    @property
    def fan_mode(self):
        return self._fan_mode

    @property
    def swing_mode(self):
        return self._swing_mode

    @property
    def min_temp(self):
        return 16.0

    @property
    def max_temp(self):
        return 32.0

    def set_temperature(self, **kwargs):
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is not None and self.min_temp <= temperature <= self.max_temp:
            self._target_temperature = temperature
            self._recently_updated = True
            self.schedule_update_ha_state()
            self._send_temperature_to_api(temperature)
        else:
            _LOGGER.error(f"Temperature {temperature} is out of range ({self.min_temp}-{self.max_temp})")

    def _send_temperature_to_api(self, temperature):
        data = {"t_temp": temperature}
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(self._api_url, json=data, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            _LOGGER.error(f"Failed to set temperature: {e}")

    async def async_set_hvac_mode(self, hvac_mode):
        self._hvac_mode = hvac_mode
        self._recently_updated = True
        self.async_write_ha_state()

        mode_mapping = {
            HVAC_MODE_FAN_ONLY: 0,
            HVAC_MODE_HEAT: 1,
            HVAC_MODE_COOL: 2,
            HVAC_MODE_DRY: 3,
            HVAC_MODE_AUTO: 4
        }

        mode = mode_mapping.get(hvac_mode, 1)
        data = {"t_work_mode": mode}
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self._api_url, json=data, headers=headers) as response:
                    response.raise_for_status()
            except aiohttp.ClientError as e:
                _LOGGER.error(f"Failed to set HVAC mode: {e}")

    async def async_set_fan_mode(self, fan_mode):
        self._fan_mode = fan_mode
        self._recently_updated = True
        self.async_write_ha_state()

        fan_mode_mapping = {
            FAN_AUTO: 0,
            FAN_LOW: 5,
            FAN_MEDIUM: 6,
            FAN_MIDDLE: 7,
            FAN_HIGH: 8,
            FAN_HIGH: 9
        }

        fan_speed = fan_mode_mapping.get(fan_mode, 0)
        data = {"t_fan_speed": fan_speed}
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self._api_url, json=data, headers=headers) as response:
                    response.raise_for_status()
            except aiohttp.ClientError as e:
                _LOGGER.error(f"Failed to set fan mode: {e}")

    async def async_set_swing_mode(self, swing_mode):
        self._swing_mode = swing_mode
        self._recently_updated = True
        self.async_write_ha_state()

        swing_mode_mapping = {
            SWING_OFF: 0,
            SWING_ON: 1
        }

        swing_direction = swing_mode_mapping.get(swing_mode, 4)
        data = {"t_up_down": swing_direction}
        headers = {'Content-Type': 'application/json'}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self._api_url, json=data, headers=headers) as response:
                    response.raise_for_status()
            except aiohttp.ClientError as e:
                _LOGGER.error(f"Failed to set swing mode: {e}")

    async def async_update(self, now=None):
        if self._recently_updated:
            self._recently_updated = False
            return

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self._get_api_url) as response:
                    response.raise_for_status()
                    data = await response.json()

                    if isinstance(data, list):
                        if len(data) > 0 and isinstance(data[0], str):
                            data = json.loads(data[0])
                        else:
                            _LOGGER.error("Expected a string inside the list from API")
                            return
                    elif isinstance(data, str):
                        data = json.loads(data)

                    status_list = data.get("statusList", {})

                    self._temperature = float(status_list.get("f_temp_in", self._temperature))
                    self._target_temperature = float(status_list.get("t_temp", self._target_temperature))
                    self._hvac_mode = self._map_hvac_mode(status_list.get("t_work_mode", str(self._hvac_mode)))
                    self._fan_mode = self._map_fan_mode(status_list.get("t_fan_speed", self._fan_mode))
                    self._swing_mode = self._map_swing_mode(status_list.get("t_up_down", self._swing_mode))

                    self.async_write_ha_state()
            except aiohttp.ClientError as e:
                _LOGGER.error(f"Failed to fetch data from API: {e}")
            except json.JSONDecodeError as e:
                _LOGGER.error(f"Failed to parse JSON data: {e}")

    def _map_hvac_mode(self, hvac_mode):
        mode_mapping = {
            "0": HVAC_MODE_FAN_ONLY,
            "1": HVAC_MODE_HEAT,
            "2": HVAC_MODE_COOL,
            "3": HVAC_MODE_DRY,
            "4": HVAC_MODE_AUTO
        }
        return mode_mapping.get(hvac_mode, HVAC_MODE_AUTO)

    def _map_fan_mode(self, fan_mode):
        fan_mode_mapping = {
            "0": FAN_AUTO,
            "5": FAN_LOW,
            "6": FAN_MEDIUM,
            "7": FAN_MIDDLE,
            "8": FAN_HIGH,
            "9": FAN_HIGH
        }
        return fan_mode_mapping.get(fan_mode, "auto")

    def _map_swing_mode(self, swing_mode):
        swing_mode_mapping = {
            "0": SWING_OFF,
            "1": SWING_ON
        }
        return swing_mode_mapping.get(swing_mode, "still")