# Todoist Integration - Changes Summary

## Files Created

### 1. `calendar_providers/todoist.py`
- New calendar provider that fetches tasks from Todoist API
- Implements the `BaseCalendarProvider` interface
- Features:
  - Fetches tasks via Todoist REST API v2
  - Converts tasks to CalendarEvent objects
  - Handles tasks with/without due dates
  - Adds priority emoji indicators (🔴🟡🔵)
  - Sorts tasks by due date
  - Caches results for 1 hour (configurable)
  - Error handling with fallback to stale cache

### 2. `test_todoist.py`
- Standalone test script to verify Todoist integration
- Checks if API token is set
- Fetches and displays tasks
- Provides helpful error messages
- Run with: `.venv/bin/python3 test_todoist.py`

### 3. `TODOIST_SETUP.md`
- Complete setup guide for Todoist integration
- Step-by-step instructions
- Troubleshooting section
- Feature documentation

### 4. `TODOIST_CHANGES.md`
- This file - documents all changes made

## Files Modified

### 1. `screen-calendar-get.py`
**Changes:**
- Added import: `from calendar_providers.todoist import TodoistCalendar`
- Added environment variable: `todoist_api_token = os.getenv("TODOIST_API_TOKEN", None)`
- Added provider selection logic (Todoist has highest priority):
  ```python
  if todoist_api_token:
      logging.info("Fetching Todoist Tasks")
      provider = TodoistCalendar(todoist_api_token, max_event_results, today_start_time, oneyearlater_iso)
  ```

### 2. `env.sh.sample`
**Changes:**
- Added Todoist configuration section:
  ```bash
  # Todoist API Token - Get it from https://todoist.com/prefs/integrations
  # export TODOIST_API_TOKEN=xxxxxxxxxxxxxx
  ```
- Placed at the top of calendar providers (highest priority)

### 3. `README.md`
**Changes:**
- Updated "Pick a Calendar provider" section
- Added Todoist as first option
- Included setup instructions
- Documented priority indicators feature

## How It Works

### Priority Order
When multiple calendar providers are configured, they are checked in this order:
1. **Todoist** (NEW - highest priority)
2. Outlook Calendar
3. CalDAV Calendar
4. ICS Calendar
5. Google Calendar (default fallback)

### Integration Flow
```
run.sh
  └─> screen-calendar-get.py
       └─> Checks TODOIST_API_TOKEN env var
            └─> If set: Uses TodoistCalendar provider
                 └─> Fetches tasks from Todoist API
                      └─> Converts to CalendarEvent objects
                           └─> Displays on e-paper screen
```

### Caching Strategy
- Tasks cached in `cache_todoist.pickle`
- Default TTL: 3600 seconds (1 hour)
- Configurable via `CALENDAR_TTL` environment variable
- On API error, falls back to stale cache if available

## Environment Variables

### Required
- `TODOIST_API_TOKEN` - Your Todoist API token

### Optional (inherited from existing system)
- `CALENDAR_TTL` - Cache duration in seconds (default: 3600)
- `LOG_LEVEL` - Logging level (default: INFO)

## Testing

### Quick Test
```bash
# Set your token
export TODOIST_API_TOKEN=your_token_here

# Run test script
.venv/bin/python3 test_todoist.py
```

### Full Integration Test
```bash
# Configure env.sh with your token
source env.sh

# Run the full display script
./run.sh
```

## Features

### Task Display
- Shows task content/summary
- Displays due dates (date only or date+time)
- Tasks without due dates shown as today's tasks
- Maximum 10 tasks displayed (configurable)

### Priority Indicators
- P1 (Priority 4 in Todoist): 🔴 Red circle
- P2 (Priority 3 in Todoist): 🟡 Yellow circle
- P3 (Priority 2 in Todoist): 🔵 Blue circle
- P4 (Priority 1 in Todoist): No indicator

### Sorting
- Tasks sorted by due date (earliest first)
- Tasks without due dates appear first

## Dependencies

No new dependencies required! Uses existing packages:
- `requests` (already in requirements.txt)
- `pickle` (Python standard library)
- `datetime` (Python standard library)

## Backward Compatibility

✅ Fully backward compatible:
- Existing calendar providers still work
- No breaking changes to existing code
- Todoist is opt-in (only used if token is set)
- Falls back to Google Calendar if no providers configured

## Next Steps

1. Get your Todoist API token
2. Add to `env.sh`: `export TODOIST_API_TOKEN=your_token`
3. Run test: `.venv/bin/python3 test_todoist.py`
4. Run display: `./run.sh`
5. Set up cron job for automation

## Notes

- Todoist API v2 is used (latest stable version)
- API endpoint: `https://api.todoist.com/rest/v2/tasks`
- Rate limits: 450 requests per 15 minutes (free tier)
- With 1-hour caching: ~24 requests/day (well within limits)
