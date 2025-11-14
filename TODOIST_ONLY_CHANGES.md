# Todoist-Only Conversion Summary

This project has been simplified to use **only Todoist** for to-do list items, removing all other calendar integrations.

## Changes Made

### 1. screen-calendar-get.py
- **Removed imports**: Google, Outlook, CalDAV, ICS calendar providers
- **Removed environment variables**: All calendar configs except `TODOIST_API_TOKEN`
- **Simplified logic**: Now only uses Todoist, throws error if token not set
- **Updated description**: Changed from "Calendar Module" to "Todoist To-Do List Module"

### 2. run.sh
- **Updated log message**: Changed "Add Calendar info" to "Add Todoist tasks"
- **Updated error message**: Changed to reflect Todoist-specific errors

### 3. README.md
- **Updated title**: Now "Todoist To-Do List" focused
- **Simplified features**: Highlights Todoist integration as primary feature
- **Removed**: References to multiple calendar providers

## What Still Works

✅ Todoist task fetching with priority indicators (🔴🟡🔵)
✅ Weather providers (Met.no, OpenWeatherMap, etc.)
✅ Web interface for configuration
✅ All 5 display layouts
✅ Cache system
✅ Privacy modes (XKCD, Literature Clock)

## What Was Removed

❌ Google Calendar integration
❌ Outlook Calendar integration
❌ CalDAV integration
❌ ICS Calendar integration
❌ Calendar provider selection logic

## How to Use

1. Get your Todoist API token from: https://todoist.com/prefs/integrations
2. Add to `env.sh`:
   ```bash
   export TODOIST_API_TOKEN="your_token_here"
   ```
3. Run: `./run.sh`

## Testing

Test your Todoist connection:
```bash
source env.sh
.venv/bin/python3 test_todoist.py
```

## Files Modified

- `screen-calendar-get.py` - Main calendar/task fetching script
- `run.sh` - Run script with updated messages
- `README.md` - Updated documentation
- `TODOIST_ONLY_CHANGES.md` - This file

## Files NOT Modified (Still Support Multiple Options)

- `web_interface.py` - Still works fine
- `templates/index.html` - Still works fine
- `calendar_providers/todoist.py` - Unchanged
- All other calendar provider files - Still exist but not used
