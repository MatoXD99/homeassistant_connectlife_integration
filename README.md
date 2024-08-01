# ConnectLife Home Assistant Integration

This integration allows you to control your ConnectLife-enabled climate devices using Home Assistant. It integrates with the Home Assistant platform, enabling you to monitor and control climate settings directly from the Home Assistant interface. It creates a climate entity, which is natively compatible with built-in and 3rd party climate cards.

[![Buy Me a Coffee](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Add%20On-blue.svg)](https://www.home-assistant.io/)

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Available API Endpoints](#available_api_endpoints)
- [Notes](#notes)
- [Support](#support)
- [License](#license)

## Prerequisites
This integration is dependent on the "Connectlife API proxy & MQTT Add-on". Ensure you have this add-on installed and configured before setting up this integration.
- [ConnectLife API proxy & MQTT Add-on](https://github.com/bilan/connectlife-api-connector)

## Installation
### Step 1: Add the Integration Repository to HACS
Open Home Assistant and navigate to HACS.
Go to Integrations.
Click on the three dots in the top right corner and select "Custom repositories".
Add the following repository URL:
```https://github.com/MatoXD99/homeassistant_connectlife_integration```
Select the category as Integration and click Add.

### Step 2: Install the Integration
Search for ConnectLife in the HACS integrations list.
Click on the ConnectLife integration and select Install.

### Step 3: Configure the Integration
After installing, navigate to Configuration > Devices & Services.
Click Add Integration and search for ConnectLife.
Select ConnectLife and follow the prompts to configure the integration (Add entity). You will need to provide the API URL and device ID, which can be obtained from the Connectlife API proxy & MQTT Add-on (I used Postman for API calls. More on that in [connectlife-api-connector](https://github.com/bilan/connectlife-api-connector).

## Configuration
### Required Configuration Parameters
- **Climate puID**: The base URL of your ConnectLife API.
- **Device ID**: The unique identifier for your ConnectLife device.
- **Update Frequency (seconds)**: How often will the data be updated (this is in case you change settings on AC with remote or ConnectLife App).
- **Port**: Specify the port on which the ConnectLife API proxy & MQTT Add-on is running.

### Example Configuration
```
  puID: pu0xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx79xx9xxx84
  Device ID: 86xxxxxxxxxxxxxxxxxxxxxxxx7xxe9xxcx4
  Update Frequency: 10
  Host: 192.168.10.15
  Port: 8000
```

## Available API Endpoints

| Function           | JSON Parameter       | Values                                               |
|--------------------|----------------------|------------------------------------------------------|
| **On/Off**         | `t_power`            | 0 (OFF), 1 (ON)                                      |
| **Temp Change**    | `t_temp`             | 16-32 (Example: 23)                                  |
| **Quiet Mode**     | `t_fan_mute`         | 0 (OFF), 1 (ON)                                      |
| **Work Mode**      | `t_work_mode`        | 0 (FAN), 1 (HEAT), 2 (COOL), 3 (DRY), 4 (AUTO)       |
| **Energy Saving**  | `t_eco`              | 0 (OFF), 1 (ON)                                      |
| **Fast Cooling**   | `t_super`            | 0 (OFF), 1 (ON)                                      |
| **Fan Speed**      | `t_fan_speed`        | 0 (AUTO), 5 (SUPER LOW), 6 (LOW), 7 (MID), 8 (HIGH), 9 (SUPER HIGH) |
| **Swing Up-Down**  | `t_up_down`          | 0 (OFF), 1 (ON)                                      |
| **GET All Data**   | `no params`          | http://0.0.0.0:8000/api/devices/device_id)					 |

## Notes
Ensure that your ConnectLife API proxy & MQTT Add-on is running and accessible from your Home Assistant instance.
The integration is designed to periodically fetch the current state of your device and update the Home Assistant interface accordingly.

## Support
For issues or questions, please open an issue on the GitHub repository. There will be bugs, especially when I might be the worst programmer in the history of programmers, but I make it work.

## Thanks
This project would not be possible without [bilan](https://github.com/bilan), who made the [connectlife-api-connector](https://github.com/bilan/connectlife-api-connector). Special thanks to you <3

## License
This project is licensed under the MIT License. See the LICENSE file for details.

