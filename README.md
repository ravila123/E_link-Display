# Waveshare ePaper Display

A feature-rich dashboard for Raspberry Pi with Waveshare 7.5" ePaper display. Shows weather, calendar events, tasks, and more on a beautiful e-ink screen.


## Features

- Multiple weather providers (OpenWeatherMap, Met Office, AccuWeather, and more)
- Calendar integration (Google, Outlook, Todoist, ICS, CalDav)
- Task management with Todoist
- Web interface for easy configuration
- Multiple layout options
- Privacy modes (XKCD comics, literature clock)
- Severe weather alerts
- Multi-language support
- Customizable fonts and data  

## Table of Contents

- [Shopping List](#shopping-list)
- [Quick Start](#quick-start)
- [Setup](#setup)
  - [Prepare the Pi](#prepare-the-pi)
  - [Connect the Display](#connect-the-display)
  - [Clone and Install](#clone-and-install)
- [Configuration](#configuration)
  - [Web Interface (Recommended)](#web-interface-recommended)
  - [Manual Configuration](#manual-configuration)
  - [Weather Providers](#weather-providers)
  - [Calendar Providers](#calendar-providers)
  - [Display Options](#display-options)
- [Running](#running)
  - [Manual Run](#manual-run)
  - [Automation](#automation)
- [Advanced Features](#advanced-features)
  - [Custom Data](#custom-data)
  - [Language Support](#language-support)
  - [Custom Fonts](#custom-fonts)
  - [Privacy Mode](#privacy-mode)
- [Troubleshooting](#troubleshooting)
- [Development](#development)


## Shopping List

- [Waveshare 7.5" ePaper Display HAT](https://www.waveshare.com/product/displays/e-paper/epaper-1/7.5inch-e-paper-hat.htm) (640x384)
- Raspberry Pi Zero WH (or any Raspberry Pi with GPIO)
- microSD card (16GB or larger recommended)
- Optional: Picture frame (7x5 inch / 18x13cm)

## Quick Start

Want to get started fast? Use the web interface:

1. Follow the [Setup](#setup) instructions below
2. Start the web interface: `.venv/bin/python3 web_interface.py`
3. Open http://raspberrypi.local:5000 in your browser
4. Configure everything through the friendly web UI

See [WEB_INTERFACE_GUIDE.md](WEB_INTERFACE_GUIDE.md) for detailed instructions.

## Setup

### Prepare the Pi

1. Use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to install Raspberry Pi OS
2. In the imager settings:
   - Set username and password
   - Enable SSH
   - Configure WiFi
3. Boot the Pi and ensure it has internet access

### Connect the Display

1. Power off the Pi
2. Attach the HAT to the GPIO pins
3. Connect the ribbon cable (lift black latch, insert ribbon, push latch down)
4. Power on and SSH into the Pi

### Clone and Install

```bash
cd ~
sudo apt update && sudo apt upgrade
sudo apt install git
git clone --recursive https://github.com/ravi/waveshare-epaper-display.git
cd waveshare-epaper-display

# Install dependencies
sudo apt install gsfonts fonts-noto python3 python3-pip pigpio libopenjp2-7 \
                 python3-venv libjpeg-dev libxslt1-dev fontconfig libcairo2

# Create virtual environment
python3 -m venv --system-site-packages .venv
.venv/bin/pip3 install -r requirements.txt

# Enable SPI
sudo raspi-config nonint do_spi 0
sudo reboot
```

## Configuration

### Web Interface (Recommended)

The easiest way to configure your display:

```bash
# Install web interface dependencies
.venv/bin/pip3 install -r requirements-web.txt

# Start the web server
.venv/bin/python3 web_interface.py
```

Then open http://raspberrypi.local:5000 in your browser and configure everything visually.

See [WEB_INTERFACE_GUIDE.md](WEB_INTERFACE_GUIDE.md) for complete documentation.

### Manual Configuration

Copy the sample environment file:

```bash
cp env.sh.sample env.sh
nano env.sh
```

#### Basic Settings

Set your Waveshare display version (1, 2, or 2B):

```bash
export WAVESHARE_EPD75_VERSION=2
```

Set your location and temperature format:

```bash
export WEATHER_LATITUDE=51.3656
export WEATHER_LONGITUDE=0.1963
export WEATHER_FORMAT=CELSIUS  # or FAHRENHEIT
```

### Weather Providers

Choose one weather provider:



#### OpenWeatherMap

1. Register at [OpenWeatherMap](https://openweathermap.org)
2. Get your API key from the [API Keys page](https://home.openweathermap.org/api_keys)
3. Add to env.sh:

```bash
export OPENWEATHERMAP_APIKEY=your_api_key
```

#### Met Office (UK)

1. Create account at [Met Office DataHub](https://datahub.metoffice.gov.uk)
2. Subscribe to 'Global Spot' under [subscriptions](https://datahub.metoffice.gov.uk/profile/subscriptions)
3. Add to env.sh:

```bash
export METOFFICEDATAHUB_API_KEY=your_api_key
```

#### AccuWeather

1. Register at [AccuWeather Developer](https://developer.accuweather.com/)
2. [Create an application](https://developer.accuweather.com/user/me/apps)
3. Get your Location Key from [AccuWeather search](https://www.accuweather.com/) (last number in URL)
4. Add to env.sh:

```bash
export ACCUWEATHER_APIKEY=your_api_key
export ACCUWEATHER_LOCATIONKEY=328328
```

#### Met.no (Norway)

Free service, just requires identification:

```bash
export METNO_SELF_IDENTIFICATION=you@example.com
```

Note: Provides 6-hour forecasts instead of full day.

#### Met Éireann (Ireland)

Free service under CC BY 4.0 license:

```bash
export WEATHER_MET_EIREANN=1
```

Note: Weather alerts must also be enabled (see alert providers below).

#### Weather.gov (US)

Free service, requires identification:

```bash
export WEATHERGOV_SELF_IDENTIFICATION=you@example.com
```

Note: API reliability may vary.

#### Climacell (tomorrow.io)

1. Register at [Climacell](https://www.climacell.co/weather-api/)
2. Add to env.sh:

```bash
export CLIMACELL_APIKEY=your_api_key
```

#### VisualCrossing

1. Register at [VisualCrossing](https://www.visualcrossing.com/)
2. Generate API key under Account Details
3. Add to env.sh:

```bash
export VISUALCROSSING_APIKEY=your_api_key
```

#### SMHI (Sweden)

Free service, requires identification:

```bash
export SMHI_SELF_IDENTIFICATION=you@example.com
```

### Severe Weather Alerts (Optional)

Configure weather alert providers to display warnings:

#### Met Office (UK)

Get your region's RSS feed from the [Met Office RSS page](https://www.metoffice.gov.uk/weather/guides/rss):

```bash
export ALERT_METOFFICE_FEED_URL=https://www.metoffice.gov.uk/public/data/PWSCache/WarningsRSS/Region/se
```

#### Weather.gov (US)

Uses your configured latitude/longitude:

```bash
export ALERT_WEATHERGOV_SELF_IDENTIFICATION=you@example.com
```

#### Met Éireann (Ireland)

Choose your region's JSON file from https://www.met.ie/Open_Data/json/:

```bash
export ALERT_MET_EIREANN_FEED_URL=https://www.met.ie/Open_Data/json/warning_EI07.json
```

### Calendar Providers

Choose one or more calendar/task providers:

#### Todoist

Popular task management with priority indicators:

1. Get your API token from [Todoist Integrations](https://todoist.com/prefs/integrations)
2. Add to env.sh:

```bash
export TODOIST_API_TOKEN=your_api_token
```

Features:
- 🔴 P1 (urgent) tasks
- 🟡 P2 (high priority) tasks
- 🔵 P3 (medium priority) tasks
- Sorted by due date
- Tasks without dates appear as today's tasks

See [TODOIST_SETUP.md](TODOIST_SETUP.md) for detailed instructions.

#### Google Calendar

1. Get your Calendar ID from [Google Calendar settings](https://calendar.google.com) (under "Integrate Calendar")
2. Add to env.sh:

```bash
export GOOGLE_CALENDAR_ID=xyz12345@group.calendar.google.com
```

3. Run OAuth flow:

```bash
.venv/bin/python3 screen-calendar-get.py
```

4. Follow the URL in your browser and log in
5. When it redirects to localhost:8080, copy that URL
6. In another SSH session, run:

```bash
curl "http://localhost:8080/..."
```

A `token.pickle` file will be created for future use.


#### Outlook Calendar

1. Run the setup script:

```bash
.venv/bin/python3 outlook_util.py
```

2. Log in with your Microsoft account
3. Copy the Calendar ID from the output
4. Add to env.sh:

```bash
export OUTLOOK_CALENDAR_ID=AQMkAxyz...
```

#### ICS Calendar

Simple URL-based calendar:

```bash
export ICS_CALENDAR_URL=https://example.com/calendar.ics
```

#### CalDav Calendar

For Nextcloud, ownCloud, etc.:

```bash
export CALDAV_CALENDAR_URL=https://nextcloud.example.com/remote.php/dav/principals/users/123456/
export CALDAV_USERNAME=username
export CALDAV_PASSWORD=password
```

Note: CalDav implementation varies by server.

### Display Options

#### Choose a Layout


Set in env.sh:

```bash
export SCREEN_LAYOUT=1  # Default
# export SCREEN_LAYOUT=2  # More calendar entries
# export SCREEN_LAYOUT=3  # Calendar on left
# export SCREEN_LAYOUT=4  # Hour display (color screens)
# export SCREEN_LAYOUT=5  # With month calendar
```

| Layout 1 (Default) | Layout 2 (More Events) |
| --- | --- |
| [![Layout 1](screenshots/001.png)](screenshots/001.png) | [![Layout 2](screenshots/002.png)](screenshots/002.png) |

| Layout 3 (Left Aligned) | Layout 4 (Color) |
| --- | --- |
| [![Layout 3](screenshots/003.png)](screenshots/003.png) | [![Layout 4](screenshots/004.png)](screenshots/004.png) |

| Layout 5 (With Month) | |
| --- | --- |
| [![Layout 5](screenshots/005.png)](screenshots/005.png) | |

## Running

### Manual Run

Test your configuration:

```bash
./run.sh
```

This will:
1. Fetch weather data
2. Fetch calendar/task data
3. Generate a PNG image
4. Convert to 1-bit BMP (for fast refresh)
5. Display on the e-paper screen

### Automation

#### Option 1: Cron Job

```bash
crontab -e
```

Add this line to run every minute:

```bash
* * * * * cd /home/pi/waveshare-epaper-display && bash run.sh > run.log 2>&1
```

#### Option 2: Systemd Timer

```bash
mkdir -p ~/.config/systemd/user/
cp waveshare-epaper-display.service.example ~/.config/systemd/user/waveshare-epaper-display.service
cp waveshare-epaper-display.timer.example ~/.config/systemd/user/waveshare-epaper-display.timer
systemctl --user daemon-reload
systemctl --user enable waveshare-epaper-display.timer
loginctl enable-linger
```

## Advanced Features

### Custom Data

Add your own data to the display (API calls, Home Assistant, PiHole stats, etc.):

1. Rename `screen-custom-get.py.sample` to `screen-custom-get.py`
2. Add your custom code and set `custom_value_1`
3. Modify `screen-custom.svg` to adjust appearance
4. Run `./run.sh`

### Language Support

The system locale determines date/time formats. Default is usually `en_GB`.

Check current locale:

```bash
locale
locale -a  # See installed locales
```

Install new locales:

```bash
sudo dpkg-reconfigure locales
```

Set in env.sh:

```bash
export LANG=ko_KR.UTF-8
```

#### Non-Western Languages

For Chinese/Japanese/Korean, install Noto fonts (already in setup). If characters don't display, set Noto as default font (see below).

### Custom Fonts

Default font is DejaVu Sans. To change to Noto Sans:

1. Check current font:

```bash
fc-match sans-serif
```

2. Install Noto fonts:

```bash
sudo apt install fonts-noto
```

3. Create font config:

```bash
mkdir -p ~/.config/fontconfig/conf.d
nano ~/.config/fontconfig/conf.d/00-fonts.conf
```

4. Add this content:

```xml
<?xml version='1.0'?>
<!DOCTYPE fontconfig SYSTEM 'fonts.dtd'>
<fontconfig>
  <alias>
    <family>sans-serif</family>
    <prefer>
        <family>Noto Sans</family>
    </prefer>
  </alias>
</fontconfig>
```

5. Verify:

```bash
fc-match sans-serif
```

### Privacy Mode

Hide all personal information and display either XKCD comics or literary quotes:

```bash
export PRIVACY_MODE_XKCD=1  # Show XKCD comic
# OR
export PRIVACY_MODE_LITERATURE_CLOCK=1  # Show time as literature quote
```

| XKCD Mode | Literature Clock |
| --- | --- |
| [![XKCD](screenshots/pvt_xkcd.png)](screenshots/pvt_xkcd.png) | [![Literature](screenshots/pvt_literature.png)](screenshots/pvt_literature.png) |



## Troubleshooting

### Check Logs

```bash
tail -f run.log
```

Enable debug logging in env.sh:

```bash
export LOG_LEVEL=DEBUG
```

### Clear Cache

Force fresh data by deleting cache files:

```bash
rm cache_weather.json
rm cache_todoist.pickle
rm cache_calendar.pickle
rm cache_outlookcalendar.pickle
```

### Re-authenticate

Delete token files to force re-login:

```bash
rm token.pickle  # Google
rm outlooktoken.bin  # Outlook
```

### Test Waveshare Display

If nothing works, test with Waveshare's official examples:

```bash
git clone https://github.com/waveshare/e-Paper
cd e-Paper
```

See [Waveshare Wiki](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT) and [user manual](https://www.waveshare.com/w/upload/7/74/7.5inch-e-paper-hat-user-manual-en.pdf).

## Development

### Local Debugging

Run and debug locally without a Raspberry Pi. The GPIO write will fail, but you can view the generated `screen-output.png`.

Setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run:

```bash
./run.sh
```

Debug in VSCode:
1. Open a Python file (e.g., `screen-calendar-get.py`)
2. Press F5
3. Set breakpoints as needed

## Additional Documentation

- [Web Interface Guide](WEB_INTERFACE_GUIDE.md) - Complete web UI documentation
- [Todoist Setup](TODOIST_SETUP.md) - Detailed Todoist integration guide
- [Changelog](CHANGELOG.md) - Version history and updates

## Author

Created and maintained by **Ravi**.

## Contributing

Contributions welcome! Please open an issue or pull request on GitHub.

## License

See [LICENSE](LICENSE) file for details.
