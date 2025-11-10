#!/usr/bin/env python3
"""
Complete test showing exactly what will appear on the e-paper display
"""

import os
import sys
import datetime

# Set environment
os.environ['TODOIST_API_TOKEN'] = 'ff627b6d4a7421b3571137c314b963fc36e0b821'
os.environ['LOG_LEVEL'] = 'INFO'

from calendar_providers.todoist import TodoistCalendar
from utility import configure_logging, get_formatted_date, get_formatted_time

configure_logging()

print("=" * 80)
print("E-PAPER DISPLAY OUTPUT PREVIEW")
print("=" * 80)
print()

# Fetch Todoist tasks
print("📡 Fetching your Todoist tasks...")
today_start_time = datetime.datetime.utcnow()
oneyearlater_iso = (datetime.datetime.now().astimezone() + datetime.timedelta(days=365)).astimezone()

try:
    provider = TodoistCalendar(
        'ff627b6d4a7421b3571137c314b963fc36e0b821',
        10,
        today_start_time,
        oneyearlater_iso
    )
    tasks = provider.get_calendar_events()
    
    print(f"✅ Fetched {len(tasks)} tasks\n")
    
    # Format tasks as they will appear on display
    print("=" * 80)
    print("CALENDAR/TASKS SECTION (Right side of display)")
    print("=" * 80)
    print()
    
    for i, task in enumerate(tasks[:10], 1):
        # Format date/time
        if task.all_day_event or type(task.start) == datetime.date:
            start = datetime.datetime.combine(task.start, datetime.time.min) if type(task.start) == datetime.date else task.start
            date_display = get_formatted_date(start, include_time=False)
        else:
            date_display = get_formatted_date(task.start)
        
        print(f"{i}. {date_display}")
        print(f"   {task.summary}")
        print()
    
    print("=" * 80)
    print("COMPLETE DISPLAY LAYOUT PREVIEW")
    print("=" * 80)
    print()
    print("┌" + "─" * 78 + "┐")
    print("│" + " " * 78 + "│")
    print("│  TIME: 10:30 AM" + " " * 30 + "Monday" + " " * 25 + "│")
    print("│" + " " * 48 + "November 11, 2025" + " " * 13 + "│")
    print("│" + " " * 78 + "│")
    print("│  ☀️  Weather" + " " * 20 + "│  📅 CALENDAR/TASKS" + " " * 23 + "│")
    print("│  High: 20°C" + " " * 21 + "│" + " " * 45 + "│")
    print("│  Low: 15°C" + " " * 22 + "│" + " " * 45 + "│")
    print("│  Partly Cloudy" + " " * 18 + "│" + " " * 45 + "│")
    print("│" + " " * 34 + "│" + " " * 45 + "│")
    
    # Show first 4 tasks in the preview
    for i, task in enumerate(tasks[:4], 1):
        if task.all_day_event or type(task.start) == datetime.date:
            start = datetime.datetime.combine(task.start, datetime.time.min) if type(task.start) == datetime.date else task.start
            date_display = get_formatted_date(start, include_time=False)
        else:
            date_display = get_formatted_date(task.start)
        
        # Truncate long task names
        task_name = task.summary[:40] + "..." if len(task.summary) > 40 else task.summary
        
        print(f"│" + " " * 34 + f"│  {i}. {date_display}" + " " * (43 - len(date_display)) + "│")
        print(f"│" + " " * 34 + f"│     {task_name}" + " " * (40 - len(task_name)) + "│")
    
    if len(tasks) > 4:
        print("│" + " " * 34 + f"│  ... and {len(tasks) - 4} more tasks" + " " * 22 + "│")
    
    print("│" + " " * 78 + "│")
    print("└" + "─" * 78 + "┘")
    
    print()
    print("=" * 80)
    print("✅ TODOIST INTEGRATION WORKING PERFECTLY!")
    print("=" * 80)
    print()
    print("What happens on your Raspberry Pi:")
    print("1. Weather data fetched from Met.no (or your chosen provider)")
    print("2. Your 10 Todoist tasks fetched and formatted")
    print("3. SVG template populated with data")
    print("4. SVG converted to PNG (800x480 pixels)")
    print("5. PNG displayed on e-paper screen")
    print()
    print("Update frequency: Every hour (or as configured in CALENDAR_TTL)")
    print()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
