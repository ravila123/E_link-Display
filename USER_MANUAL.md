---
title: "Waveshare E-Paper Display System"
subtitle: "Complete User Manual & Technical Documentation"
version: "2.0"
date: "November 2025"
author: "E-Paper Display Project"
---

# Waveshare E-Paper Display System
## Complete User Manual & Technical Documentation

**Version 2.0 | November 2025**

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [System Overview](#2-system-overview)
3. [Hardware Requirements](#3-hardware-requirements)
4. [Initial Setup](#4-initial-setup)
5. [Software Installation](#5-software-installation)
6. [Configuration Guide](#6-configuration-guide)
7. [Web Interface](#7-web-interface)
8. [Weather Providers](#8-weather-providers)
9. [Calendar & Task Integration](#9-calendar--task-integration)
10. [Display Layouts](#10-display-layouts)
11. [Advanced Features](#11-advanced-features)
12. [Automation & Scheduling](#12-automation--scheduling)
13. [Troubleshooting](#13-troubleshooting)
14. [Technical Reference](#14-technical-reference)
15. [Maintenance & Updates](#15-maintenance--updates)
16. [Appendix](#16-appendix)

---


## 1. Introduction

### 1.1 About This System

The Waveshare E-Paper Display System is a comprehensive dashboard solution designed for Raspberry Pi single-board computers. It transforms a 7.5-inch e-paper display into an elegant information center that shows:

- **Real-time weather information** with forecasts and alerts
- **Calendar events** from multiple sources
- **Task management** with priority indicators
- **Custom data** from various APIs and services

The system features low power consumption, excellent readability in all lighting conditions, and a paper-like appearance that blends seamlessly into any environment.

### 1.2 Key Features

#### Display Capabilities
- **Multiple layouts** - Choose from 5 different screen layouts
- **High contrast** - E-ink technology provides excellent readability
- **Low power** - Display retains image without power
- **Customizable** - Extensive configuration options

#### Integration Support
- **Weather Services** - 9+ weather providers including OpenWeatherMap, Met Office, AccuWeather
- **Calendar Systems** - Google Calendar, Outlook, ICS, CalDAV
- **Task Management** - Todoist integration with priority indicators
- **Alerts** - Severe weather warnings and notifications

#### User Interface
- **Web-based configuration** - Easy setup through browser
- **Command-line tools** - Advanced control for power users
- **Automated updates** - Scheduled refresh via cron or systemd
- **Real-time logs** - Monitor system activity

### 1.3 System Requirements

#### Minimum Requirements
- Raspberry Pi Zero WH or newer
- Waveshare 7.5" E-Paper Display HAT
- 8GB microSD card
- Internet connection (WiFi or Ethernet)
- Power supply (5V, 2.5A recommended)

#### Recommended Requirements
- Raspberry Pi 3B+ or newer
- 16GB+ microSD card (Class 10)
- Stable internet connection
- Quality power supply with surge protection

### 1.4 Document Conventions

Throughout this manual, the following conventions are used:


**Code blocks** - Commands to be entered in terminal:
```bash
sudo apt update
```

**File paths** - Referenced as `~/waveshare-epaper-display/env.sh`

**Configuration values** - Shown as `VARIABLE_NAME=value`

**Notes** - Important information highlighted with ℹ️

**Warnings** - Critical information marked with ⚠️

**Tips** - Helpful suggestions indicated with 💡

---

## 2. System Overview

### 2.1 Architecture

The system consists of several interconnected components:

```
┌─────────────────────────────────────────────────────┐
│                  User Interface                      │
│  ┌──────────────────┐    ┌──────────────────┐      │
│  │  Web Interface   │    │  Command Line    │      │
│  │  (Port 5000)     │    │  (SSH/Terminal)  │      │
│  └──────────────────┘    └──────────────────┘      │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│              Configuration Layer                     │
│                   (env.sh)                          │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│               Data Collection                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ Weather  │  │ Calendar │  │  Tasks   │         │
│  │ Provider │  │ Provider │  │ Provider │         │
│  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│            Image Generation                          │
│         (SVG → PNG → BMP)                           │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│          Display Controller                          │
│        (SPI Communication)                           │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│         E-Paper Display                              │
│         (7.5" E-Ink)                                │
└─────────────────────────────────────────────────────┘
```

### 2.2 Data Flow

1. **Configuration** - System reads settings from `env.sh`
2. **Data Fetching** - Retrieves weather, calendar, and task data
3. **Caching** - Stores data locally to reduce API calls
4. **Rendering** - Generates SVG template with data
5. **Conversion** - Converts SVG → PNG → 1-bit BMP
6. **Display** - Sends image to e-paper via SPI
7. **Sleep** - Display enters low-power mode

### 2.3 File Structure


```
waveshare-epaper-display/
├── env.sh                          # Main configuration file
├── run.sh                          # Main execution script
├── display.py                      # Display controller
├── web_interface.py                # Web UI server
│
├── weather_providers/              # Weather data sources
│   ├── openweathermap.py
│   ├── metoffice.py
│   └── ...
│
├── calendar_providers/             # Calendar integrations
│   ├── google.py
│   ├── outlook.py
│   ├── todoist.py
│   └── ...
│
├── alert_providers/                # Weather alert sources
│   └── ...
│
├── templates/                      # Web interface templates
│   └── index.html
│
├── screenshots/                    # Example images
├── icons/                         # Weather icons
├── lib/                           # Waveshare library
│
├── cache_*.pickle                 # Cached data files
├── run.log                        # System logs
└── screen-output.png              # Generated image
```

---

## 3. Hardware Requirements

### 3.1 Required Components

#### 3.1.1 Raspberry Pi
**Supported Models:**
- Raspberry Pi Zero WH (minimum)
- Raspberry Pi Zero 2 W
- Raspberry Pi 3 Model B/B+
- Raspberry Pi 4 Model B (recommended)
- Raspberry Pi 5

**Specifications:**
- ARM processor (any generation)
- Minimum 512MB RAM
- GPIO header (40-pin)
- WiFi capability (or Ethernet adapter)

#### 3.1.2 Waveshare E-Paper Display
**Compatible Models:**
- 7.5" E-Paper HAT (640×384) - Version 1
- 7.5" E-Paper HAT (800×480) - Version 2
- 7.5" E-Paper HAT B (Red/Black/White) - Version 2B

**Display Specifications:**
- Resolution: 640×384 or 800×480 pixels
- Colors: Black/White or Black/Red/White
- Viewing angle: >170°
- Refresh time: ~15 seconds
- Interface: SPI
- Power: <0.05W (standby)


#### 3.1.3 Storage
**MicroSD Card:**
- Minimum: 8GB
- Recommended: 16GB or larger
- Class: Class 10 or UHS-I
- Brand: SanDisk, Samsung, or Kingston recommended

#### 3.1.4 Power Supply
**Requirements:**
- Voltage: 5V DC
- Current: 2.5A minimum (3A recommended)
- Connector: USB-C (Pi 4/5) or Micro-USB (older models)
- Quality: Official Raspberry Pi power supply recommended

⚠️ **Warning:** Inadequate power supply can cause system instability, display errors, and SD card corruption.

### 3.2 Optional Components

#### 3.2.1 Enclosure/Frame
- Picture frame (7×5 inch / 18×13 cm)
- 3D-printed case
- Acrylic stand
- Wall mount bracket

#### 3.2.2 Accessories
- Heatsinks for Raspberry Pi
- Cooling fan (for Pi 4/5)
- Surge protector
- Backup power supply

### 3.3 Hardware Assembly

#### Step 1: Prepare the Raspberry Pi
1. Insert microSD card into card slot
2. Ensure GPIO pins are clean and straight
3. Do not power on yet

#### Step 2: Attach the E-Paper HAT
1. **Power off** the Raspberry Pi completely
2. Align the HAT with GPIO pins (Pin 1 to Pin 1)
3. Gently press down until fully seated
4. Ensure all 40 pins are connected

⚠️ **Caution:** Never attach or remove the HAT while powered on. This can damage both devices.

#### Step 3: Connect the Display
1. Locate the ribbon cable connector on the HAT
2. Lift the black latch on the connector
3. Insert ribbon cable with contacts facing down
4. Push latch down to secure cable
5. Verify cable is firmly seated

#### Step 4: Physical Installation
1. Place assembly in frame or enclosure
2. Ensure adequate ventilation
3. Route power cable safely
4. Secure all components

💡 **Tip:** Test the system before final installation to ensure everything works correctly.

---


## 4. Initial Setup

### 4.1 Raspberry Pi OS Installation

#### 4.1.1 Download Raspberry Pi Imager
1. Visit https://www.raspberrypi.com/software/
2. Download for your operating system (Windows/Mac/Linux)
3. Install the application

#### 4.1.2 Prepare the SD Card
1. Insert microSD card into computer
2. Launch Raspberry Pi Imager
3. Click "Choose OS"
4. Select "Raspberry Pi OS (64-bit)" or "Raspberry Pi OS Lite"
5. Click "Choose Storage"
6. Select your microSD card

⚠️ **Warning:** This will erase all data on the SD card.

#### 4.1.3 Configure Settings
1. Click the gear icon (⚙️) for advanced options
2. **Set hostname:** `raspberrypi` (or custom name)
3. **Enable SSH:** Check "Enable SSH"
4. **Set username:** `pi` (or custom)
5. **Set password:** Choose a strong password
6. **Configure WiFi:**
   - SSID: Your network name
   - Password: Your WiFi password
   - Country: Your country code
7. **Set locale:** Your timezone and keyboard layout
8. Click "Save"

#### 4.1.4 Write Image
1. Click "Write"
2. Confirm the operation
3. Wait for writing and verification (5-10 minutes)
4. Safely eject the SD card

### 4.2 First Boot

#### 4.2.1 Power On
1. Insert SD card into Raspberry Pi
2. Connect power supply
3. Wait 2-3 minutes for first boot
4. Green LED should blink (activity indicator)

#### 4.2.2 Find IP Address
**Method 1: Router Admin Panel**
- Log into your router
- Look for device named "raspberrypi"
- Note the IP address

**Method 2: Network Scanner**
- Use tool like Angry IP Scanner or Fing
- Scan your local network
- Look for Raspberry Pi device

**Method 3: mDNS (Recommended)**
- Most systems support `raspberrypi.local`
- No IP address needed

#### 4.2.3 SSH Connection
**From Windows:**
```bash
ssh pi@raspberrypi.local
# Or: ssh pi@192.168.1.xxx
```

**From Mac/Linux:**
```bash
ssh pi@raspberrypi.local
```

Enter the password you set during imaging.


### 4.3 System Update

After connecting via SSH, update the system:

```bash
# Update package lists
sudo apt update

# Upgrade installed packages
sudo apt upgrade -y

# Reboot if kernel was updated
sudo reboot
```

Wait 1-2 minutes, then reconnect via SSH.

### 4.4 Enable SPI Interface

The e-paper display requires SPI to be enabled:

```bash
# Enable SPI
sudo raspi-config nonint do_spi 0

# Verify SPI is enabled
lsmod | grep spi
```

You should see `spi_bcm2835` or similar in the output.

---

## 5. Software Installation

### 5.1 Install System Dependencies

```bash
# Navigate to home directory
cd ~

# Install required packages
sudo apt install -y \
    git \
    python3 \
    python3-pip \
    python3-venv \
    gsfonts \
    fonts-noto \
    pigpio \
    libopenjp2-7 \
    libjpeg-dev \
    libxslt1-dev \
    fontconfig \
    libcairo2

# Verify installation
python3 --version
git --version
```

Expected output:
- Python 3.9 or newer
- Git 2.x or newer

### 5.2 Clone Repository

```bash
# Clone the project with submodules
git clone --recursive https://github.com/ravi/waveshare-epaper-display.git

# Navigate to project directory
cd waveshare-epaper-display

# Verify files
ls -la
```

You should see files like `run.sh`, `display.py`, `env.sh.sample`, etc.

### 5.3 Create Virtual Environment

```bash
# Create Python virtual environment
python3 -m venv --system-site-packages .venv

# Activate virtual environment
source .venv/bin/activate

# Verify activation (prompt should show (.venv))
which python3
```


### 5.4 Install Python Dependencies

```bash
# Install core dependencies
.venv/bin/pip3 install -r requirements.txt

# Install web interface dependencies (optional)
.venv/bin/pip3 install -r requirements-web.txt

# Verify installation
.venv/bin/pip3 list
```

This installs packages including:
- Pillow (image processing)
- CairoSVG (SVG rendering)
- Requests (HTTP client)
- Flask (web interface)
- And more...

### 5.5 Initial Configuration

```bash
# Copy sample configuration
cp env.sh.sample env.sh

# Make run script executable
chmod +x run.sh

# Edit configuration
nano env.sh
```

At minimum, set:
- `WAVESHARE_EPD75_VERSION` (1, 2, or 2B)
- `WEATHER_LATITUDE` (your location)
- `WEATHER_LONGITUDE` (your location)

Save with `Ctrl+O`, exit with `Ctrl+X`.

### 5.6 Verify Installation

```bash
# Test the system (without display update)
.venv/bin/python3 --version

# Check if all modules load
.venv/bin/python3 -c "import PIL, cairosvg, requests; print('OK')"
```

If you see "OK", installation is successful.

---

## 6. Configuration Guide

### 6.1 Configuration File Overview

The `env.sh` file contains all system settings. It uses bash environment variable syntax:

```bash
export VARIABLE_NAME="value"
```

### 6.2 Essential Settings

#### 6.2.1 Display Configuration

```bash
# Display version (REQUIRED)
export WAVESHARE_EPD75_VERSION="2"
# Options: "1" (640×384), "2" (800×480), "2B" (color)

# Screen layout (OPTIONAL)
export SCREEN_LAYOUT="1"
# Options: 1-5 (see section 10 for details)
```

#### 6.2.2 Location Settings

```bash
# Geographic coordinates (REQUIRED for weather)
export WEATHER_LATITUDE="51.5077"
export WEATHER_LONGITUDE="-0.1277"

# Temperature format (OPTIONAL)
export WEATHER_FORMAT="CELSIUS"
# Options: "CELSIUS" or "FAHRENHEIT"
```


#### 6.2.3 Cache Settings

```bash
# Weather cache duration (seconds)
export WEATHER_TTL="3600"
# Default: 3600 (1 hour)

# Calendar cache duration (seconds)
export CALENDAR_TTL="3600"
# Default: 3600 (1 hour)
```

💡 **Tip:** Longer cache times reduce API calls but show older data.

#### 6.2.4 Logging

```bash
# Log verbosity level
export LOG_LEVEL="INFO"
# Options: DEBUG, INFO, WARNING, ERROR
```

### 6.3 Finding Your Coordinates

**Method 1: Google Maps**
1. Open https://maps.google.com
2. Right-click your location
3. Click the coordinates to copy
4. Format: `51.5077, -0.1277`

**Method 2: GPS Device**
- Use smartphone GPS app
- Note latitude and longitude

**Method 3: Online Tools**
- Visit https://www.latlong.net
- Search for your location

### 6.4 Configuration Validation

After editing `env.sh`, validate the configuration:

```bash
# Load configuration
source env.sh

# Check variables are set
echo "Display Version: $WAVESHARE_EPD75_VERSION"
echo "Latitude: $WEATHER_LATITUDE"
echo "Longitude: $WEATHER_LONGITUDE"
```

---

## 7. Web Interface

### 7.1 Overview

The web interface provides a user-friendly way to configure the system without editing files manually.

**Features:**
- Visual configuration forms
- Real-time status monitoring
- One-click display updates
- Log viewer
- Cache management

### 7.2 Starting the Web Interface

```bash
# Navigate to project directory
cd ~/waveshare-epaper-display

# Start web server
.venv/bin/python3 web_interface.py
```

Expected output:
```
 * Running on http://0.0.0.0:5000
 * Running on http://192.168.1.xxx:5000
```

Leave this terminal open. The server runs in foreground.


### 7.3 Accessing the Interface

**From same device:**
```
http://localhost:5000
```

**From another device on network:**
```
http://raspberrypi.local:5000
```

**Using IP address:**
```
http://192.168.1.xxx:5000
```

### 7.4 Interface Sections

#### 7.4.1 Status Dashboard
Displays:
- Last update timestamp
- Number of cache files
- Log file size

#### 7.4.2 Configuration Form
**Todoist Integration:**
- API token input
- Link to get token

**Weather Configuration:**
- Provider selection
- Location coordinates
- Temperature format

**Display Settings:**
- Waveshare version
- Screen layout
- Cache duration
- Log level

#### 7.4.3 Action Buttons
- **Update Display Now** - Triggers immediate refresh
- **Clear Cache** - Removes all cached data
- **View Logs** - Shows recent log entries

### 7.5 Making Configuration Changes

1. Open web interface in browser
2. Modify desired settings
3. Click "💾 Save Configuration"
4. Wait for success message
5. Click "🔄 Update Display Now" to apply

### 7.6 Running as Background Service

To keep web interface running permanently:

```bash
# Create systemd service file
sudo nano /etc/systemd/system/epaper-web.service
```

Add this content:
```ini
[Unit]
Description=E-Paper Display Web Interface
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/waveshare-epaper-display
ExecStart=/home/pi/waveshare-epaper-display/.venv/bin/python3 web_interface.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable epaper-web
sudo systemctl start epaper-web
sudo systemctl status epaper-web
```

---


## 8. Weather Providers

### 8.1 Provider Comparison

| Provider | Cost | API Key | Coverage | Features |
|----------|------|---------|----------|----------|
| Met.no | Free | Email only | Global | 6-hour forecast |
| OpenWeatherMap | Free tier | Yes | Global | Full day forecast |
| Met Office | Free | Yes | UK focus | Detailed UK data |
| AccuWeather | Free tier | Yes | Global | Location-based |
| VisualCrossing | Free tier | Yes | Global | Historical data |
| Weather.gov | Free | Email only | US only | Government data |
| Met Éireann | Free | No | Ireland | Official Irish data |
| SMHI | Free | Email only | Sweden | Swedish data |
| Climacell | Paid | Yes | Global | Advanced features |

### 8.2 Met.no (Recommended for Beginners)

**Advantages:**
- Completely free
- No API key required
- Global coverage
- Reliable service

**Setup:**
```bash
# Edit configuration
nano env.sh

# Add this line
export METNO_SELF_IDENTIFICATION="your.email@example.com"

# Save and exit
```

**Requirements:**
- Valid email address (for identification)
- Latitude and longitude coordinates

**Limitations:**
- 6-hour forecast only (not full day)
- Basic weather data

### 8.3 OpenWeatherMap

**Advantages:**
- Free tier available (1000 calls/day)
- Full day forecasts
- Extensive weather data
- Well-documented API

**Setup:**

**Step 1: Create Account**
1. Visit https://openweathermap.org
2. Click "Sign Up"
3. Complete registration
4. Verify email address

**Step 2: Get API Key**
1. Log in to account
2. Go to https://home.openweathermap.org/api_keys
3. Copy your API key (or create new one)

**Step 3: Configure**
```bash
nano env.sh

# Add this line
export OPENWEATHERMAP_APIKEY="your_api_key_here"
```

**Step 4: Test**
```bash
source env.sh
.venv/bin/python3 screen-weather-get.py
```


### 8.4 Met Office (UK)

**Best for:** UK residents wanting detailed local forecasts

**Setup:**

**Step 1: Create Account**
1. Visit https://datahub.metoffice.gov.uk
2. Register for account
3. Verify email

**Step 2: Subscribe to API**
1. Go to https://datahub.metoffice.gov.uk/profile/subscriptions
2. Find "Site Specific" product
3. Subscribe to "Global Spot" (free)
4. Copy API key

**Step 3: Configure**
```bash
nano env.sh

export METOFFICEDATAHUB_API_KEY="your_api_key_here"
```

### 8.5 AccuWeather

**Setup:**

**Step 1: Developer Account**
1. Visit https://developer.accuweather.com
2. Register account
3. Create new application
   - Name: "Personal Display"
   - Type: "Limited Trial"
   - Category: "Internal App"

**Step 2: Get Location Key**
1. Go to https://www.accuweather.com
2. Search for your location
3. Note the number in URL
   - Example: `.../london/ec4a-2/weather-forecast/328328`
   - Location Key: `328328`

**Step 3: Configure**
```bash
nano env.sh

export ACCUWEATHER_APIKEY="your_api_key"
export ACCUWEATHER_LOCATIONKEY="328328"
```

### 8.6 Weather Alerts

Some providers support severe weather warnings:

**Met Office (UK):**
```bash
export ALERT_METOFFICE_FEED_URL="https://www.metoffice.gov.uk/public/data/PWSCache/WarningsRSS/Region/se"
```

Find your region at: https://www.metoffice.gov.uk/weather/guides/rss

**Weather.gov (US):**
```bash
export ALERT_WEATHERGOV_SELF_IDENTIFICATION="your@email.com"
```

**Met Éireann (Ireland):**
```bash
export ALERT_MET_EIREANN_FEED_URL="https://www.met.ie/Open_Data/json/warning_EI07.json"
```

---


## 9. Calendar & Task Integration

### 9.1 Todoist (Recommended)

**Advantages:**
- Simple setup (just API token)
- Priority indicators (🔴🟡🔵)
- Task management features
- Automatic sorting by due date

**Setup:**

**Step 1: Get API Token**
1. Log in to https://todoist.com
2. Go to Settings → Integrations
3. Or visit: https://todoist.com/prefs/integrations
4. Scroll to "API token"
5. Click to reveal and copy token

**Step 2: Configure**
```bash
nano env.sh

export TODOIST_API_TOKEN="your_token_here"
```

**Step 3: Test**
```bash
source env.sh
.venv/bin/python3 test_todoist.py
```

**Features:**
- 🔴 P1 (Priority 4) - Urgent tasks
- 🟡 P2 (Priority 3) - High priority
- 🔵 P3 (Priority 2) - Medium priority
- Tasks sorted by due date
- Shows date and time for tasks

### 9.2 Google Calendar

**Setup:**

**Step 1: Get Calendar ID**
1. Open https://calendar.google.com
2. Click settings (⚙️) → Settings
3. Select your calendar from left sidebar
4. Scroll to "Integrate calendar"
5. Copy "Calendar ID"
   - Format: `xyz12345@group.calendar.google.com`
   - Or use `primary` for main calendar

**Step 2: Configure**
```bash
nano env.sh

export GOOGLE_CALENDAR_ID="xyz12345@group.calendar.google.com"
# Or for primary calendar:
export GOOGLE_CALENDAR_ID="primary"
```

**Step 3: OAuth Authentication**
```bash
.venv/bin/python3 screen-calendar-get.py
```

This will:
1. Display a long URL
2. Open URL in browser
3. Log in to Google account
4. Grant calendar access
5. Redirect to `http://localhost:8080/...`

**Step 4: Complete Authentication**

The redirect will fail (expected). Copy the full URL from browser.

In another SSH session:
```bash
curl "http://localhost:8080/?code=..."
```

A `token.pickle` file will be created. Future runs won't require authentication.


### 9.3 Outlook Calendar

**Setup:**

**Step 1: Run Setup Script**
```bash
.venv/bin/python3 outlook_util.py
```

**Step 2: Authenticate**
1. Script will display a URL
2. Open URL in browser
3. Log in with Microsoft account
4. Accept permissions
5. Wait for script to complete

**Step 3: Select Calendar**
Script will display available calendars:
```
Calendar: Work
ID: AQMkADAwATM0MDAAMS...

Calendar: Personal
ID: AQMkADAwATM0MDAAMS...
```

Copy the ID of desired calendar.

**Step 4: Configure**
```bash
nano env.sh

export OUTLOOK_CALENDAR_ID="AQMkADAwATM0MDAAMS..."
```

### 9.4 ICS Calendar

**For:** Public calendars, shared calendars, exported .ics files

**Setup:**
```bash
nano env.sh

export ICS_CALENDAR_URL="https://example.com/calendar.ics"
```

**Examples:**
- Google Calendar public link
- Outlook shared calendar
- Apple Calendar published link
- Any HTTP-accessible .ics file

⚠️ **Note:** No authentication supported. Calendar must be publicly accessible.

### 9.5 CalDAV Calendar

**For:** Nextcloud, ownCloud, Synology, other CalDAV servers

**Setup:**
```bash
nano env.sh

export CALDAV_CALENDAR_URL="https://nextcloud.example.com/remote.php/dav/principals/users/username/"
export CALDAV_USERNAME="your_username"
export CALDAV_PASSWORD="your_password"
```

**Finding CalDAV URL:**

**Nextcloud:**
1. Settings → Calendar
2. Click calendar settings (⚙️)
3. Copy CalDAV link

**Synology:**
- Format: `https://nas.example.com:5006/caldav/username/`

ℹ️ **Note:** CalDAV implementation varies by server. Some features may not work.

### 9.6 Calendar Priority

If multiple calendars are configured, priority order:
1. Todoist (highest)
2. Outlook
3. CalDAV
4. ICS
5. Google (default)

Only one calendar source is used at a time.

---


## 10. Display Layouts

### 10.1 Layout Overview

The system offers 5 different screen layouts to suit various preferences and use cases.

### 10.2 Layout 1 (Default)

**Configuration:**
```bash
export SCREEN_LAYOUT="1"
```

**Features:**
- Large time display
- Prominent weather information
- Date and day of week
- 5-6 calendar entries
- Weather icon
- High/low temperature

**Best for:**
- General purpose use
- Balanced information display
- Easy readability from distance

**Screen Division:**
```
┌─────────────────────────────────────┐
│  Date                    Weather    │
│  Day of Week             Icon       │
│                          Hi/Lo      │
│                                     │
│         LARGE TIME                  │
│                                     │
│  ─────────────────────────────────  │
│  Calendar Event 1                   │
│  Calendar Event 2                   │
│  Calendar Event 3                   │
│  Calendar Event 4                   │
│  Calendar Event 5                   │
└─────────────────────────────────────┘
```

### 10.3 Layout 2 (More Calendar)

**Configuration:**
```bash
export SCREEN_LAYOUT="2"
```

**Features:**
- Smaller time display
- More space for calendar entries
- 8-10 calendar entries
- Compact weather info

**Best for:**
- Heavy calendar users
- Many daily events
- Task-focused display

**Screen Division:**
```
┌─────────────────────────────────────┐
│  Time    Date    Weather            │
│  ─────────────────────────────────  │
│  Calendar Event 1                   │
│  Calendar Event 2                   │
│  Calendar Event 3                   │
│  Calendar Event 4                   │
│  Calendar Event 5                   │
│  Calendar Event 6                   │
│  Calendar Event 7                   │
│  Calendar Event 8                   │
│  Calendar Event 9                   │
│  Calendar Event 10                  │
└─────────────────────────────────────┘
```


### 10.4 Layout 3 (Calendar Left)

**Configuration:**
```bash
export SCREEN_LAYOUT="3"
```

**Features:**
- Calendar on left side
- Time and weather on right
- Vertical split design
- 6-8 calendar entries

**Best for:**
- Aesthetic preference
- Wall-mounted displays
- Balanced layout

**Screen Division:**
```
┌──────────────────┬──────────────────┐
│ Calendar Event 1 │                  │
│ Calendar Event 2 │      TIME        │
│ Calendar Event 3 │                  │
│ Calendar Event 4 │  ─────────────   │
│ Calendar Event 5 │                  │
│ Calendar Event 6 │     Weather      │
│ Calendar Event 7 │     Icon         │
│ Calendar Event 8 │     Hi/Lo        │
└──────────────────┴──────────────────┘
```

### 10.5 Layout 4 (Color Display)

**Configuration:**
```bash
export SCREEN_LAYOUT="4"
```

**Features:**
- Designed for color e-paper (2B version)
- Hour-by-hour forecast
- Graphical weather display
- Optimized for red/black/white

**Best for:**
- Waveshare 7.5" B displays
- Weather-focused information
- Visual appeal

⚠️ **Requires:** `WAVESHARE_EPD75_VERSION="2B"`

### 10.6 Layout 5 (With Month Calendar)

**Configuration:**
```bash
export SCREEN_LAYOUT="5"
```

**Features:**
- Mini month calendar
- Current day highlighted
- Calendar events listed
- At-a-glance date reference

**Best for:**
- Date-aware users
- Planning and scheduling
- Month overview needed

**Screen Division:**
```
┌──────────────────┬──────────────────┐
│ Calendar Event 1 │   November 2025  │
│ Calendar Event 2 │ Su Mo Tu We Th..│
│ Calendar Event 3 │  1  2  3  4  5..│
│ Calendar Event 4 │  8  9 [10] 11..  │
│ Calendar Event 5 │                  │
│ Calendar Event 6 │     Weather      │
│                  │     Icon         │
│      TIME        │     Hi/Lo        │
└──────────────────┴──────────────────┘
```

### 10.7 Changing Layouts

**Method 1: Edit Configuration**
```bash
nano env.sh
# Change SCREEN_LAYOUT value
# Save and exit
./run.sh
```

**Method 2: Web Interface**
1. Open web interface
2. Select layout from dropdown
3. Click "Save Configuration"
4. Click "Update Display Now"

**Method 3: Command Line**
```bash
export SCREEN_LAYOUT="3"
./run.sh
```

---


## 11. Advanced Features

### 11.1 Privacy Mode

Hide personal information and display alternative content.

#### 11.1.1 XKCD Mode

Display random XKCD comics instead of personal data.

**Configuration:**
```bash
export PRIVACY_MODE_XKCD="1"
```

**Features:**
- Random XKCD comic
- Updates with each refresh
- No personal information shown
- Great for public displays

#### 11.1.2 Literature Clock Mode

Show current time as quotes from literature.

**Configuration:**
```bash
export PRIVACY_MODE_LITERATURE_CLOCK="1"
```

**Features:**
- Time shown as literary quotes
- Quotes match current time
- Artistic and unique
- Privacy-friendly

⚠️ **Note:** Only one privacy mode can be active at a time.

### 11.2 Custom Data Integration

Add your own data sources to the display.

**Step 1: Create Custom Script**
```bash
cp screen-custom-get.py.sample screen-custom-get.py
nano screen-custom-get.py
```

**Step 2: Add Your Code**
```python
# Example: Home Assistant temperature
import requests

response = requests.get('http://homeassistant.local:8123/api/states/sensor.temperature')
data = response.json()

output_dict = {
    'custom_value_1': f"{data['state']}°C",
    'custom_value_2': 'Living Room'
}
```

**Step 3: Customize Display**
```bash
nano screen-custom.svg
```

Modify SVG elements to position your custom data.

**Examples:**
- Home Assistant sensors
- PiHole statistics
- Stock prices
- Cryptocurrency values
- Server status
- Custom APIs


### 11.3 Multi-Language Support

The system supports multiple languages for date/time display.

**Step 1: Install Locale**
```bash
sudo dpkg-reconfigure locales
```

Select desired locales (choose UTF-8 versions):
- `en_GB.UTF-8` - English (UK)
- `en_US.UTF-8` - English (US)
- `de_DE.UTF-8` - German
- `fr_FR.UTF-8` - French
- `es_ES.UTF-8` - Spanish
- `ja_JP.UTF-8` - Japanese
- `ko_KR.UTF-8` - Korean
- `zh_CN.UTF-8` - Chinese (Simplified)

**Step 2: Configure**
```bash
nano env.sh

export LANG="de_DE.UTF-8"
```

**Step 3: Test**
```bash
source env.sh
./run.sh
```

Date and time will display in selected language.

### 11.4 Custom Fonts

Change the display font for different languages or aesthetics.

**Step 1: Install Font**
```bash
# Example: Noto Sans
sudo apt install fonts-noto

# Verify installation
fc-list | grep Noto
```

**Step 2: Create Font Configuration**
```bash
mkdir -p ~/.config/fontconfig/conf.d
nano ~/.config/fontconfig/conf.d/00-fonts.conf
```

**Step 3: Set Font Preference**
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

**Step 4: Verify**
```bash
fc-match sans-serif
```

Should show: `NotoSans-Regular.ttf`

**Recommended Fonts:**
- **Western languages:** DejaVu Sans (default)
- **CJK languages:** Noto Sans CJK
- **Arabic:** Noto Sans Arabic
- **Monospace:** Noto Sans Mono

---


## 12. Automation & Scheduling

### 12.1 Manual Execution

Run the display update manually:

```bash
cd ~/waveshare-epaper-display
./run.sh
```

This will:
1. Fetch weather data
2. Fetch calendar/task data
3. Generate image
4. Update display
5. Log results to `run.log`

### 12.2 Cron Job (Recommended)

Automate updates using cron.

**Step 1: Edit Crontab**
```bash
crontab -e
```

**Step 2: Add Schedule**

**Every minute:**
```cron
* * * * * cd /home/pi/waveshare-epaper-display && bash run.sh > run.log 2>&1
```

**Every 5 minutes:**
```cron
*/5 * * * * cd /home/pi/waveshare-epaper-display && bash run.sh > run.log 2>&1
```

**Every 15 minutes:**
```cron
*/15 * * * * cd /home/pi/waveshare-epaper-display && bash run.sh > run.log 2>&1
```

**Every hour:**
```cron
0 * * * * cd /home/pi/waveshare-epaper-display && bash run.sh > run.log 2>&1
```

**Specific times (8 AM, 12 PM, 6 PM):**
```cron
0 8,12,18 * * * cd /home/pi/waveshare-epaper-display && bash run.sh > run.log 2>&1
```

**Step 3: Verify Cron**
```bash
crontab -l
```

**Step 4: Check Logs**
```bash
tail -f ~/waveshare-epaper-display/run.log
```

### 12.3 Systemd Timer (Alternative)

More reliable than cron for some use cases.

**Step 1: Create Service File**
```bash
mkdir -p ~/.config/systemd/user/
nano ~/.config/systemd/user/waveshare-epaper-display.service
```

**Content:**
```ini
[Unit]
Description=Waveshare E-Paper Display Update
After=network.target

[Service]
Type=oneshot
WorkingDirectory=/home/pi/waveshare-epaper-display
ExecStart=/home/pi/waveshare-epaper-display/run.sh
StandardOutput=append:/home/pi/waveshare-epaper-display/run.log
StandardError=append:/home/pi/waveshare-epaper-display/run.log

[Install]
WantedBy=default.target
```

**Step 2: Create Timer File**
```bash
nano ~/.config/systemd/user/waveshare-epaper-display.timer
```

**Content:**
```ini
[Unit]
Description=Waveshare E-Paper Display Timer
Requires=waveshare-epaper-display.service

[Timer]
OnBootSec=1min
OnUnitActiveSec=5min
Unit=waveshare-epaper-display.service

[Install]
WantedBy=timers.target
```


**Step 3: Enable and Start**
```bash
systemctl --user daemon-reload
systemctl --user enable waveshare-epaper-display.timer
systemctl --user start waveshare-epaper-display.timer
loginctl enable-linger
```

**Step 4: Check Status**
```bash
systemctl --user status waveshare-epaper-display.timer
systemctl --user list-timers
```

**Step 5: Manual Trigger**
```bash
systemctl --user start waveshare-epaper-display.service
```

### 12.4 Update Frequency Recommendations

**Considerations:**
- E-paper refresh time (~15 seconds)
- API rate limits
- Power consumption
- Display wear

**Recommended Frequencies:**

| Use Case | Frequency | Reason |
|----------|-----------|--------|
| Home dashboard | 15 minutes | Balance updates/wear |
| Office display | 30 minutes | Reduce wear |
| Public display | 1 hour | Minimal wear |
| Weather station | 5 minutes | Frequent updates |
| Calendar focus | 10 minutes | Event changes |

💡 **Tip:** E-paper displays have limited refresh cycles (typically 1 million+). More frequent updates = shorter display lifespan.

### 12.5 Conditional Updates

Update only when data changes:

**Create wrapper script:**
```bash
nano ~/waveshare-epaper-display/smart-update.sh
```

**Content:**
```bash
#!/bin/bash
cd ~/waveshare-epaper-display

# Generate new image
./run.sh --no-display

# Compare with previous
if ! cmp -s screen-output.png screen-output-prev.png; then
    # Images differ, update display
    python3 display.py screen-output.png
    cp screen-output.png screen-output-prev.png
fi
```

**Make executable:**
```bash
chmod +x ~/waveshare-epaper-display/smart-update.sh
```

**Use in cron:**
```cron
*/5 * * * * ~/waveshare-epaper-display/smart-update.sh
```

---


## 13. Troubleshooting

### 13.1 Display Issues

#### Problem: Display shows nothing
**Possible causes:**
- Display not powered
- Ribbon cable loose
- SPI not enabled
- Wrong display version

**Solutions:**
```bash
# Check SPI is enabled
lsmod | grep spi

# Enable SPI if needed
sudo raspi-config nonint do_spi 0
sudo reboot

# Verify display version in env.sh
cat env.sh | grep WAVESHARE_EPD75_VERSION

# Test with Waveshare examples
cd ~/waveshare-epaper-display/lib/e-Paper/RaspberryPi_JetsonNano/python/examples
python3 epd_7in5_V2_test.py
```

#### Problem: Display shows partial image
**Possible causes:**
- Insufficient power
- Corrupted image file
- Display hardware issue

**Solutions:**
```bash
# Check power supply (should be 5V, 2.5A+)
vcgencmd get_throttled
# 0x0 = good, anything else = power issue

# Regenerate image
rm screen-output.png screen-output.bmp
./run.sh

# Check image file
file screen-output.png
identify screen-output.png
```

#### Problem: Display updates slowly
**Expected behavior:**
- E-paper refresh takes 10-20 seconds
- This is normal for e-ink technology

**To improve:**
- Use 1-bit BMP (already default)
- Reduce image complexity
- Ensure adequate power

### 13.2 Weather Data Issues

#### Problem: No weather data
**Check:**
```bash
# Verify API key is set
source env.sh
echo $OPENWEATHERMAP_APIKEY

# Test weather fetch
.venv/bin/python3 screen-weather-get.py

# Check cache file
cat cache_weather.json
```

**Common issues:**
- Invalid API key
- API rate limit exceeded
- Network connectivity
- Incorrect coordinates

#### Problem: Wrong location weather
**Solution:**
```bash
# Verify coordinates
source env.sh
echo "Lat: $WEATHER_LATITUDE"
echo "Lon: $WEATHER_LONGITUDE"

# Test coordinates online
# Visit: https://www.google.com/maps/@$WEATHER_LATITUDE,$WEATHER_LONGITUDE,15z
```


### 13.3 Calendar/Task Issues

#### Problem: No calendar events showing
**Check:**
```bash
# Test calendar fetch
.venv/bin/python3 screen-calendar-get.py

# Check cache
ls -lh cache_*.pickle

# Verify token exists
ls -lh token.pickle outlooktoken.bin
```

**For Todoist:**
```bash
# Test Todoist connection
.venv/bin/python3 test_todoist.py

# Verify API token
source env.sh
echo $TODOIST_API_TOKEN
```

**For Google Calendar:**
```bash
# Re-authenticate
rm token.pickle
.venv/bin/python3 screen-calendar-get.py
```

#### Problem: Old events showing
**Solution:**
```bash
# Clear cache
rm cache_*.pickle

# Force update
./run.sh
```

### 13.4 System Issues

#### Problem: Script fails to run
**Check logs:**
```bash
tail -50 run.log
```

**Common errors:**

**"Module not found"**
```bash
# Reinstall dependencies
.venv/bin/pip3 install -r requirements.txt
```

**"Permission denied"**
```bash
# Fix permissions
chmod +x run.sh
chmod +x display.py
```

**"No space left on device"**
```bash
# Check disk space
df -h

# Clean up
sudo apt clean
rm cache_*.pickle
rm *.log
```

#### Problem: High CPU usage
**Causes:**
- Image generation is CPU-intensive
- Normal during update

**Monitor:**
```bash
top
htop  # if installed
```

**Reduce load:**
- Increase update interval
- Use simpler layout
- Reduce image quality


### 13.5 Network Issues

#### Problem: Cannot connect to APIs
**Diagnose:**
```bash
# Test internet connectivity
ping -c 4 8.8.8.8

# Test DNS
ping -c 4 google.com

# Test specific API
curl -I https://api.openweathermap.org
```

**Solutions:**
```bash
# Restart networking
sudo systemctl restart networking

# Check WiFi
iwconfig

# Reconnect WiFi
sudo raspi-config
# Select: System Options → Wireless LAN
```

### 13.6 Web Interface Issues

#### Problem: Cannot access web interface
**Check:**
```bash
# Verify server is running
ps aux | grep web_interface

# Check port
sudo netstat -tulpn | grep 5000

# Test locally
curl http://localhost:5000
```

**Firewall:**
```bash
# Check firewall
sudo ufw status

# Allow port if needed
sudo ufw allow 5000/tcp
```

**Access from network:**
```bash
# Find IP address
hostname -I

# Test from another device
# http://192.168.1.xxx:5000
```

### 13.7 Getting Help

**Check logs:**
```bash
# System log
tail -100 run.log

# Enable debug logging
nano env.sh
# Add: export LOG_LEVEL="DEBUG"
./run.sh
tail -100 run.log
```

**Collect system info:**
```bash
# System details
uname -a
cat /etc/os-release

# Python version
python3 --version

# Installed packages
.venv/bin/pip3 list

# Display version
source env.sh
echo $WAVESHARE_EPD75_VERSION
```

**Community support:**
- GitHub Issues: https://github.com/ravi/waveshare-epaper-display/issues
- Check existing issues first
- Provide logs and system info
- Include configuration (remove API keys!)

---


## 14. Technical Reference

### 14.1 System Architecture

#### 14.1.1 Software Stack
```
┌─────────────────────────────────────┐
│     Application Layer               │
│  (Python Scripts, Web Interface)    │
├─────────────────────────────────────┤
│     Framework Layer                 │
│  (Flask, PIL, CairoSVG, Requests)   │
├─────────────────────────────────────┤
│     System Layer                    │
│  (Python 3.9+, Linux Libraries)     │
├─────────────────────────────────────┤
│     Hardware Layer                  │
│  (SPI, GPIO, E-Paper Controller)    │
└─────────────────────────────────────┘
```

#### 14.1.2 Data Flow Diagram
```
External APIs → Data Fetchers → Cache → SVG Generator
                                           ↓
Display ← SPI Driver ← Image Converter ← PNG Renderer
```

### 14.2 File Reference

#### 14.2.1 Core Scripts

**run.sh**
- Main execution script
- Orchestrates all components
- Handles error checking
- Logs output

**display.py**
- Display controller
- SPI communication
- Image buffer management
- Power management

**screen-weather-get.py**
- Weather data fetcher
- Provider abstraction
- Cache management
- Error handling

**screen-calendar-get.py**
- Calendar data fetcher
- Multiple provider support
- Event parsing
- Date formatting

**web_interface.py**
- Flask web server
- Configuration management
- Real-time updates
- Log viewing

#### 14.2.2 Configuration Files

**env.sh**
- Main configuration
- Environment variables
- API keys and tokens
- System settings

**env.sh.sample**
- Template configuration
- Example values
- Documentation


### 14.3 SPI Communication

#### 14.3.1 Pin Configuration

| GPIO Pin | Function | Description |
|----------|----------|-------------|
| GPIO 10 | MOSI | Master Out Slave In (Data to display) |
| GPIO 9 | MISO | Master In Slave Out (Data from display) |
| GPIO 11 | SCLK | Serial Clock |
| GPIO 8 | CE0 | Chip Enable 0 |
| GPIO 25 | DC | Data/Command Select |
| GPIO 17 | RST | Reset |
| GPIO 24 | BUSY | Busy Signal |

#### 14.3.2 SPI Parameters

```python
SPI_BUS = 0
SPI_DEVICE = 0
SPI_SPEED = 4000000  # 4 MHz
SPI_MODE = 0b00      # Mode 0 (CPOL=0, CPHA=0)
```

#### 14.3.3 Communication Protocol

**Initialization Sequence:**
1. Assert RST (reset display)
2. Wait for BUSY to clear
3. Send initialization commands
4. Configure display parameters

**Display Update Sequence:**
1. Send DATA_START_TRANSMISSION command
2. Transfer image buffer via SPI
3. Send DISPLAY_REFRESH command
4. Wait for BUSY to clear
5. Enter sleep mode

**Command Structure:**
```
DC=LOW  → Command byte
DC=HIGH → Data byte
```

### 14.4 Image Processing Pipeline

#### 14.4.1 SVG Generation
```python
# Template: screen-template.{layout}.svg
# Variables replaced: {{time}}, {{date}}, {{weather}}, etc.
# Output: screen-template-output.svg
```

#### 14.4.2 SVG to PNG Conversion
```python
# Tool: CairoSVG
# Resolution: 800×480 or 640×384
# Format: RGB PNG
# Output: screen-output.png
```

#### 14.4.3 PNG to BMP Conversion
```python
# Tool: PIL (Pillow)
# Conversion: RGB → 1-bit monochrome
# Dithering: Floyd-Steinberg
# Output: screen-output.bmp
```

#### 14.4.4 BMP to Display Buffer
```python
# Tool: Waveshare EPD library
# Format: Byte array
# Size: (width × height) / 8 bytes
# Transfer: Via SPI
```


### 14.5 API Rate Limits

| Provider | Free Tier Limit | Recommended Cache |
|----------|----------------|-------------------|
| OpenWeatherMap | 1,000 calls/day | 1 hour |
| Met Office | 360 calls/hour | 1 hour |
| AccuWeather | 50 calls/day | 2 hours |
| Todoist | 450 calls/15min | 1 hour |
| Google Calendar | 1,000,000 calls/day | 30 minutes |
| Met.no | Unlimited* | 30 minutes |

*Subject to fair use policy

### 14.6 Performance Metrics

**Typical Update Times:**

| Operation | Duration |
|-----------|----------|
| Weather API call | 0.5-2 seconds |
| Calendar API call | 0.5-3 seconds |
| SVG generation | 0.1-0.5 seconds |
| PNG rendering | 1-3 seconds |
| BMP conversion | 0.5-1 second |
| Display refresh | 10-20 seconds |
| **Total** | **15-30 seconds** |

**Resource Usage:**

| Resource | Idle | During Update |
|----------|------|---------------|
| CPU | <5% | 50-100% |
| RAM | 50-100 MB | 150-250 MB |
| Disk I/O | Minimal | Moderate |
| Network | None | 10-50 KB |

### 14.7 Power Consumption

| Component | Power Draw |
|-----------|------------|
| Raspberry Pi Zero W | 0.5-1.0 W |
| Raspberry Pi 4 | 2.5-3.5 W |
| E-Paper Display (active) | 0.5-1.0 W |
| E-Paper Display (standby) | <0.05 W |
| **Total (Pi Zero)** | **1.0-2.0 W** |
| **Total (Pi 4)** | **3.0-4.5 W** |

**Annual Energy Cost:**
- Pi Zero: ~$2-4 USD/year
- Pi 4: ~$6-10 USD/year
(Based on $0.12/kWh)

---

## 15. Maintenance & Updates

### 15.1 Regular Maintenance

#### 15.1.1 Weekly Tasks
```bash
# Check logs for errors
tail -100 ~/waveshare-epaper-display/run.log

# Verify display is updating
ls -lh ~/waveshare-epaper-display/screen-output.png

# Check disk space
df -h
```

#### 15.1.2 Monthly Tasks
```bash
# Update system packages
sudo apt update
sudo apt upgrade -y

# Clean package cache
sudo apt clean
sudo apt autoremove -y

# Check Python dependencies
cd ~/waveshare-epaper-display
.venv/bin/pip3 list --outdated
```


#### 15.1.3 Quarterly Tasks
```bash
# Backup configuration
cp ~/waveshare-epaper-display/env.sh ~/env.sh.backup

# Update project
cd ~/waveshare-epaper-display
git pull
git submodule update --init --recursive

# Reinstall dependencies
.venv/bin/pip3 install -r requirements.txt --upgrade
```

### 15.2 Backup Procedures

#### 15.2.1 Configuration Backup
```bash
# Backup env.sh
cp ~/waveshare-epaper-display/env.sh ~/backup/env.sh.$(date +%Y%m%d)

# Backup tokens
cp ~/waveshare-epaper-display/token.pickle ~/backup/
cp ~/waveshare-epaper-display/outlooktoken.bin ~/backup/
```

#### 15.2.2 Full System Backup
```bash
# Create SD card image (from another computer)
# Linux/Mac:
sudo dd if=/dev/sdX of=~/raspberrypi-backup.img bs=4M status=progress

# Windows: Use Win32DiskImager or similar
```

#### 15.2.3 Cloud Backup
```bash
# Install rclone
curl https://rclone.org/install.sh | sudo bash

# Configure cloud storage
rclone config

# Backup configuration
rclone copy ~/waveshare-epaper-display/env.sh remote:backup/
```

### 15.3 Software Updates

#### 15.3.1 Update Project Code
```bash
cd ~/waveshare-epaper-display

# Check for updates
git fetch
git status

# Update to latest
git pull origin main
git submodule update --init --recursive

# Reinstall dependencies
.venv/bin/pip3 install -r requirements.txt --upgrade

# Test
./run.sh
```

#### 15.3.2 Update Python Packages
```bash
cd ~/waveshare-epaper-display

# List outdated packages
.venv/bin/pip3 list --outdated

# Update specific package
.venv/bin/pip3 install --upgrade package_name

# Update all packages (use with caution)
.venv/bin/pip3 install --upgrade -r requirements.txt
```

#### 15.3.3 Update Raspberry Pi OS
```bash
# Update package lists
sudo apt update

# Upgrade packages
sudo apt upgrade -y

# Upgrade distribution (major updates)
sudo apt full-upgrade -y

# Reboot if needed
sudo reboot
```


### 15.4 Display Care

#### 15.4.1 E-Paper Display Lifespan
- Typical lifespan: 1-2 million refreshes
- At 1 refresh/minute: ~2-4 years
- At 1 refresh/15 minutes: ~30-60 years

#### 15.4.2 Best Practices
- Avoid excessive refresh rates
- Don't display static images for months
- Perform full refresh periodically (built-in at 2 AM)
- Keep display clean and dry
- Avoid extreme temperatures

#### 15.4.3 Cleaning
- Power off system
- Use soft, dry microfiber cloth
- For stubborn marks: slightly damp cloth
- Never use chemicals or abrasives
- Let dry completely before powering on

### 15.5 Troubleshooting Updates

#### Problem: Update breaks system
**Solution:**
```bash
# Revert to previous version
cd ~/waveshare-epaper-display
git log --oneline  # Find previous commit
git checkout <commit-hash>

# Or restore from backup
cp ~/backup/env.sh ~/waveshare-epaper-display/
```

#### Problem: Dependencies conflict
**Solution:**
```bash
# Recreate virtual environment
cd ~/waveshare-epaper-display
rm -rf .venv
python3 -m venv --system-site-packages .venv
.venv/bin/pip3 install -r requirements.txt
```

---

## 16. Appendix

### 16.1 Glossary

**API (Application Programming Interface)**
- Interface for software to communicate with services

**BMP (Bitmap)**
- Uncompressed image format used for display

**Cache**
- Temporary storage of data to reduce API calls

**CalDAV**
- Calendar protocol used by Nextcloud, ownCloud

**Cron**
- Time-based job scheduler in Unix-like systems

**E-Ink / E-Paper**
- Electronic paper display technology

**GPIO (General Purpose Input/Output)**
- Pins on Raspberry Pi for hardware communication

**HAT (Hardware Attached on Top)**
- Raspberry Pi expansion board

**ICS (iCalendar)**
- Standard calendar file format

**OAuth**
- Authorization protocol for API access

**PNG (Portable Network Graphics)**
- Compressed image format

**SPI (Serial Peripheral Interface)**
- Communication protocol for display

**SSH (Secure Shell)**
- Encrypted remote access protocol

**SVG (Scalable Vector Graphics)**
- XML-based vector image format

**Systemd**
- System and service manager for Linux

**TTL (Time To Live)**
- Duration data remains in cache


### 16.2 Environment Variables Reference

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `WAVESHARE_EPD75_VERSION` | String | "2" | Display version (1, 2, 2B) |
| `SCREEN_LAYOUT` | Integer | 1 | Layout number (1-5) |
| `WEATHER_LATITUDE` | Float | - | Location latitude |
| `WEATHER_LONGITUDE` | Float | - | Location longitude |
| `WEATHER_FORMAT` | String | "CELSIUS" | Temperature unit |
| `WEATHER_TTL` | Integer | 3600 | Weather cache duration (seconds) |
| `CALENDAR_TTL` | Integer | 3600 | Calendar cache duration (seconds) |
| `LOG_LEVEL` | String | "INFO" | Logging verbosity |
| `TODOIST_API_TOKEN` | String | - | Todoist API token |
| `OPENWEATHERMAP_APIKEY` | String | - | OpenWeatherMap API key |
| `METNO_SELF_IDENTIFICATION` | String | - | Met.no email |
| `GOOGLE_CALENDAR_ID` | String | "primary" | Google Calendar ID |
| `OUTLOOK_CALENDAR_ID` | String | - | Outlook Calendar ID |
| `ICS_CALENDAR_URL` | String | - | ICS calendar URL |
| `CALDAV_CALENDAR_URL` | String | - | CalDAV server URL |
| `CALDAV_USERNAME` | String | - | CalDAV username |
| `CALDAV_PASSWORD` | String | - | CalDAV password |
| `PRIVACY_MODE_XKCD` | Integer | 0 | Enable XKCD mode (0/1) |
| `PRIVACY_MODE_LITERATURE_CLOCK` | Integer | 0 | Enable literature clock (0/1) |

### 16.3 Command Reference

#### System Commands
```bash
# Update display
./run.sh

# Test weather fetch
.venv/bin/python3 screen-weather-get.py

# Test calendar fetch
.venv/bin/python3 screen-calendar-get.py

# Test Todoist
.venv/bin/python3 test_todoist.py

# Start web interface
.venv/bin/python3 web_interface.py

# View logs
tail -f run.log

# Clear cache
rm cache_*.pickle cache_*.json
```

#### Maintenance Commands
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Update project
git pull && git submodule update --init --recursive

# Reinstall dependencies
.venv/bin/pip3 install -r requirements.txt --upgrade

# Check disk space
df -h

# Check memory
free -h

# Check CPU temperature
vcgencmd measure_temp
```


### 16.4 Quick Reference Card

#### Essential Configuration
```bash
# Display version
export WAVESHARE_EPD75_VERSION="2"

# Location
export WEATHER_LATITUDE="51.5077"
export WEATHER_LONGITUDE="-0.1277"

# Weather provider (choose one)
export METNO_SELF_IDENTIFICATION="your@email.com"
# OR
export OPENWEATHERMAP_APIKEY="your_key"

# Calendar/Tasks (choose one)
export TODOIST_API_TOKEN="your_token"
# OR
export GOOGLE_CALENDAR_ID="primary"
```

#### Common Tasks
```bash
# Manual update
cd ~/waveshare-epaper-display && ./run.sh

# View logs
tail -50 ~/waveshare-epaper-display/run.log

# Clear cache
rm ~/waveshare-epaper-display/cache_*

# Web interface
.venv/bin/python3 web_interface.py
# Then visit: http://raspberrypi.local:5000
```

#### Troubleshooting Quick Checks
```bash
# Check SPI
lsmod | grep spi

# Check power
vcgencmd get_throttled

# Check network
ping -c 4 8.8.8.8

# Check disk space
df -h

# Check logs
tail -50 run.log
```

### 16.5 Resources

#### Official Documentation
- **Project Repository:** https://github.com/ravi/waveshare-epaper-display
- **Waveshare Wiki:** https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT
- **Raspberry Pi Docs:** https://www.raspberrypi.com/documentation/

#### API Documentation
- **OpenWeatherMap:** https://openweathermap.org/api
- **Todoist:** https://developer.todoist.com
- **Google Calendar:** https://developers.google.com/calendar
- **Met Office:** https://datahub.metoffice.gov.uk/docs

#### Community
- **GitHub Issues:** https://github.com/ravi/waveshare-epaper-display/issues
- **Raspberry Pi Forums:** https://forums.raspberrypi.com
- **Reddit:** r/raspberry_pi

#### Tools
- **Raspberry Pi Imager:** https://www.raspberrypi.com/software/
- **PuTTY (Windows SSH):** https://www.putty.org
- **Angry IP Scanner:** https://angryip.org


### 16.6 Frequently Asked Questions

**Q: How long does the display last?**
A: E-paper displays typically last 1-2 million refreshes. With updates every 15 minutes, expect 2-4 years of continuous use.

**Q: Can I use this without internet?**
A: No, internet is required to fetch weather and calendar data. However, cached data will display if connection is temporarily lost.

**Q: Does the display consume power when not updating?**
A: E-paper displays retain their image without power. Only the Raspberry Pi consumes power continuously (~1-3W).

**Q: Can I display custom information?**
A: Yes! Use the custom data feature (section 11.2) to add your own data sources.

**Q: Which weather provider is best?**
A: Met.no is recommended for beginners (free, no API key). OpenWeatherMap offers more features with free tier.

**Q: Can I use multiple calendars?**
A: The system uses one calendar source at a time, with priority: Todoist > Outlook > CalDAV > ICS > Google.

**Q: How do I update the software?**
A: Run `git pull` in the project directory, then `git submodule update --init --recursive`.

**Q: Can I run this on Raspberry Pi 5?**
A: Yes, all Raspberry Pi models with 40-pin GPIO are supported.

**Q: What if my display shows garbage?**
A: Check power supply (needs 2.5A+), verify SPI is enabled, and ensure correct display version is set.

**Q: Can I access the web interface remotely?**
A: Yes, but consider security. Use VPN, reverse proxy with authentication, or port forwarding carefully.

---

## Document Information

**Version:** 2.0  
**Last Updated:** November 2025  
**Author:** E-Paper Display Project Contributors  
**License:** See project LICENSE file  

**Changelog:**
- v2.0 (Nov 2025): Added Todoist integration, web interface, comprehensive troubleshooting
- v1.5 (Jul 2024): Added privacy modes, multiple layouts
- v1.0 (Apr 2021): Initial release

---

## Support & Contributing

### Getting Help
1. Check this manual's troubleshooting section
2. Search existing GitHub issues
3. Create new issue with:
   - System information
   - Configuration (remove API keys!)
   - Log output
   - Steps to reproduce

### Contributing
Contributions welcome! Please:
- Fork the repository
- Create feature branch
- Test thoroughly
- Submit pull request
- Follow existing code style

### Reporting Bugs
Include:
- Raspberry Pi model
- OS version (`cat /etc/os-release`)
- Python version (`python3 --version`)
- Display version
- Complete error message
- Relevant log output

---

**Thank you for using the Waveshare E-Paper Display System!**

For the latest updates and documentation, visit:
https://github.com/ravi/waveshare-epaper-display

---

*End of User Manual*
