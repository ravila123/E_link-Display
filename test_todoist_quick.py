#!/usr/bin/env python3
"""Quick test to fetch Todoist tasks"""

import requests
import json
from datetime import datetime

# Your API token
TODOIST_API_TOKEN = "ff627b6d4a7421b3571137c314b963fc36e0b821"

print("=" * 70)
print("TODOIST INTEGRATION TEST")
print("=" * 70)
print()

try:
    # Fetch tasks from Todoist API
    headers = {
        "Authorization": f"Bearer {TODOIST_API_TOKEN}"
    }
    
    print("📡 Fetching tasks from Todoist API...")
    response = requests.get(
        "https://api.todoist.com/rest/v2/tasks",
        headers=headers
    )
    response.raise_for_status()
    tasks = response.json()
    
    print(f"✅ Successfully fetched {len(tasks)} tasks\n")
    
    if len(tasks) == 0:
        print("⚠️  No tasks found in your Todoist account.")
        print("   Add some tasks with due dates to see them on the display!")
    else:
        print("📋 YOUR TASKS (as they will appear on the display):")
        print("=" * 70)
        
        # Sort by due date
        tasks_with_due = [t for t in tasks if t.get('due')]
        tasks_without_due = [t for t in tasks if not t.get('due')]
        
        # Sort tasks with due dates
        tasks_with_due.sort(key=lambda x: x['due'].get('date', ''))
        
        all_tasks = tasks_with_due + tasks_without_due
        
        for i, task in enumerate(all_tasks[:10], 1):  # Show max 10 like the display
            # Priority indicator
            priority = task.get('priority', 1)
            if priority == 4:
                indicator = "🔴"
            elif priority == 3:
                indicator = "🟡"
            elif priority == 2:
                indicator = "🔵"
            else:
                indicator = "  "
            
            # Task content
            content = task.get('content', 'Untitled Task')
            
            # Due date
            due = task.get('due')
            if due:
                due_date_str = due.get('date')
                due_datetime = due.get('datetime')
                
                if due_datetime:
                    # Has specific time
                    due_display = due_datetime.replace('T', ' ').replace('Z', '')
                elif due_date_str:
                    # Just date
                    due_display = due_date_str
                else:
                    due_display = "Today"
            else:
                due_display = "No due date (shown as today)"
            
            print(f"\n{i}. {indicator} {content}")
            print(f"   📅 {due_display}")
            
            # Show project if available
            if task.get('project_id'):
                print(f"   📁 Project ID: {task.get('project_id')}")
        
        if len(tasks) > 10:
            print(f"\n... and {len(tasks) - 10} more tasks (only first 10 shown on display)")
    
    print("\n" + "=" * 70)
    print("✅ TODOIST INTEGRATION IS WORKING!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Add this to env.sh:")
    print(f"   export TODOIST_API_TOKEN={TODOIST_API_TOKEN}")
    print("2. Run: source env.sh")
    print("3. Run: ./run.sh")
    print("\nYour tasks will appear on the e-paper display! 🎉")
    
except requests.exceptions.HTTPError as e:
    print(f"❌ HTTP Error: {e}")
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.text}")
    if response.status_code == 401:
        print("\n⚠️  Authentication failed. Please check your API token.")
    elif response.status_code == 403:
        print("\n⚠️  Access forbidden. Your token may not have the right permissions.")
except requests.exceptions.RequestException as e:
    print(f"❌ Network Error: {e}")
    print("   Please check your internet connection.")
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
    import traceback
    traceback.print_exc()

print()
