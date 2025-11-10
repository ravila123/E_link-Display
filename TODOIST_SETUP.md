# Todoist Integration Setup Guide

This guide will help you set up Todoist as your calendar/task provider for the e-paper display.

## Step 1: Get Your Todoist API Token

1. Log in to [Todoist](https://todoist.com)
2. Go to **Settings** → **Integrations** (or visit https://todoist.com/prefs/integrations)
3. Scroll down to find **API token**
4. Click to reveal and copy your token

## Step 2: Configure Environment Variables

1. Copy the sample environment file (if you haven't already):
   ```bash
   cp env.sh.sample env.sh
   ```

2. Edit `env.sh`:
   ```bash
   nano env.sh
   ```

3. Add your Todoist API token:
   ```bash
   export TODOIST_API_TOKEN=your_api_token_here
   ```

4. Make sure to comment out other calendar providers (Google, Outlook, etc.) if you only want Todoist:
   ```bash
   # export GOOGLE_CALENDAR_ID=primary
   # export OUTLOOK_CALENDAR_ID=AQMkAxyz...
   ```

5. Configure weather provider (required - see main README.md)

6. Save and exit (Ctrl+O, Enter, Ctrl+X in nano)

## Step 3: Load Environment Variables

```bash
source env.sh
```

## Step 4: Test the Integration

Run the test script to verify everything works:

```bash
.venv/bin/python3 test_todoist.py
```

You should see:
- ✓ Your API token is recognized
- ✓ Your tasks are fetched successfully
- A list of your upcoming tasks

## Step 5: Run the Display Script

Once the test passes, run the full script:

```bash
./run.sh
```

This will:
1. Fetch weather data
2. Fetch your Todoist tasks
3. Generate the display image
4. Update your e-paper display

## Features

### Priority Indicators
Tasks are displayed with emoji indicators based on priority:
- 🔴 P1 (Urgent/Priority 1)
- 🟡 P2 (High/Priority 2)
- 🔵 P3 (Medium/Priority 3)
- No indicator for P4 (Low/Priority 4)

### Due Dates
- Tasks with specific times show the date and time
- All-day tasks show just the date
- Tasks without due dates appear as today's tasks

### Sorting
Tasks are automatically sorted by due date, with earliest tasks first.

### Caching
Task data is cached for 1 hour by default (configurable via `CALENDAR_TTL` in env.sh).

## Troubleshooting

### "TODOIST_API_TOKEN not set"
- Make sure you ran `source env.sh`
- Check that the token is correctly set in env.sh

### "Error fetching Todoist tasks"
- Verify your API token is correct
- Check your internet connection
- Ensure Todoist API is accessible (not blocked by firewall)

### Tasks not showing up
- Check that tasks have due dates set in Todoist
- Tasks without due dates will appear as today's tasks
- Only the first 10 tasks are displayed (configurable in screen-calendar-get.py)

### Want to show more/fewer tasks?
Edit `screen-calendar-get.py` and change:
```python
max_event_results = 10  # Change this number
```

## Automation

Once everything works, set up a cron job to update automatically:

```bash
crontab -e
```

Add this line to update every 20 minutes:
```bash
*/20 * * * * cd /home/pi/waveshare-epaper-display && bash run.sh > run.log 2>&1
```

## API Rate Limits

Todoist API has generous rate limits:
- 450 requests per 15 minutes for free users
- With 1-hour caching, you'll make ~24 requests per day
- Well within the free tier limits

## Need Help?

- Check the main README.md for general setup
- Review run.log for error messages
- Ensure all dependencies are installed (see requirements.txt)
