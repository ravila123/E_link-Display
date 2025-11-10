#!/usr/bin/env python3
"""
Simple test script to verify Todoist integration
Run this to test your Todoist API token before running the full display script
"""

import os
import sys
import datetime
from calendar_providers.todoist import TodoistCalendar
from utility import configure_logging

configure_logging()

# Get API token from environment
todoist_api_token = os.getenv("TODOIST_API_TOKEN")

if not todoist_api_token:
    print("❌ ERROR: TODOIST_API_TOKEN not set in environment")
    print("\nTo fix this:")
    print("1. Get your API token from https://todoist.com/prefs/integrations")
    print("2. Add to env.sh: export TODOIST_API_TOKEN=your_token_here")
    print("3. Run: source env.sh")
    print("4. Run this script again")
    sys.exit(1)

print("✓ Found TODOIST_API_TOKEN")
print(f"  Token: {todoist_api_token[:10]}...{todoist_api_token[-4:]}")
print()

# Test fetching tasks
print("Fetching tasks from Todoist...")
today_start_time = datetime.datetime.utcnow()
oneyearlater_iso = (datetime.datetime.now().astimezone() + datetime.timedelta(days=365)).astimezone()

try:
    provider = TodoistCalendar(todoist_api_token, 10, today_start_time, oneyearlater_iso)
    tasks = provider.get_calendar_events()
    
    print(f"✓ Successfully fetched {len(tasks)} tasks\n")
    
    if len(tasks) == 0:
        print("No tasks found. Add some tasks in Todoist and try again!")
    else:
        print("Your upcoming tasks:")
        print("-" * 60)
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task.summary}")
            if task.all_day_event:
                print(f"   Due: {task.start}")
            else:
                print(f"   Due: {task.start.strftime('%Y-%m-%d %H:%M')}")
            print()
    
    print("✓ Todoist integration is working correctly!")
    print("\nYou can now run ./run.sh to update your display")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("\nPlease check:")
    print("1. Your API token is correct")
    print("2. You have internet connection")
    print("3. Todoist API is accessible")
    sys.exit(1)
