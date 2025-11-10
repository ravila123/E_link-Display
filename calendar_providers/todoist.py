#!/usr/bin/python3
import datetime
import logging
import os
import pickle
from calendar_providers.base_provider import BaseCalendarProvider, CalendarEvent
from utility import is_stale
import requests

ttl = float(os.getenv("CALENDAR_TTL", 1 * 60 * 60))


class TodoistCalendar(BaseCalendarProvider):
    def __init__(self, todoist_api_token, max_event_results, from_date, to_date):
        self.todoist_api_token = todoist_api_token
        self.max_event_results = max_event_results
        self.from_date = from_date
        self.to_date = to_date

    def get_calendar_events(self) -> list[CalendarEvent]:
        calendar_events = []
        todoist_calendar_pickle = 'cache_todoist.pickle'

        if is_stale(os.getcwd() + "/" + todoist_calendar_pickle, ttl):
            logging.debug("Cache is stale, calling the Todoist API")

            try:
                # Fetch tasks from Todoist API
                headers = {
                    "Authorization": f"Bearer {self.todoist_api_token}"
                }
                
                response = requests.get(
                    "https://api.todoist.com/rest/v2/tasks",
                    headers=headers
                )
                response.raise_for_status()
                tasks = response.json()

                logging.debug(f"Fetched {len(tasks)} tasks from Todoist")

                # Convert Todoist tasks to CalendarEvent objects
                for task in tasks[:self.max_event_results]:
                    summary = task.get('content', 'Untitled Task')
                    
                    # Handle due date
                    due = task.get('due')
                    if due:
                        due_date_str = due.get('date')
                        due_datetime = due.get('datetime')
                        
                        if due_datetime:
                            # Task has specific time
                            start_date = datetime.datetime.fromisoformat(due_datetime.replace('Z', '+00:00'))
                            end_date = start_date + datetime.timedelta(hours=1)  # Default 1 hour duration
                            is_all_day = False
                        elif due_date_str:
                            # Task has only date (all-day)
                            start_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
                            end_date = start_date
                            is_all_day = True
                        else:
                            # No due date, use today
                            start_date = datetime.datetime.now().date()
                            end_date = start_date
                            is_all_day = True
                    else:
                        # No due date, use today
                        start_date = datetime.datetime.now().date()
                        end_date = start_date
                        is_all_day = True

                    # Add priority indicator to summary
                    priority = task.get('priority', 1)
                    if priority == 4:
                        summary = "🔴 " + summary  # P1 - Urgent
                    elif priority == 3:
                        summary = "🟡 " + summary  # P2 - High
                    elif priority == 2:
                        summary = "🔵 " + summary  # P3 - Medium

                    calendar_events.append(CalendarEvent(summary, start_date, end_date, is_all_day))

                # Sort by due date - convert dates to datetime for comparison
                def sort_key(event):
                    if event.start is None:
                        return datetime.datetime.max
                    if isinstance(event.start, datetime.date) and not isinstance(event.start, datetime.datetime):
                        return datetime.datetime.combine(event.start, datetime.time.min)
                    return event.start
                
                calendar_events.sort(key=sort_key)

                # Cache the results
                with open(todoist_calendar_pickle, 'wb') as cal:
                    pickle.dump(calendar_events, cal)

            except Exception as e:
                logging.error(f"Error fetching Todoist tasks: {e}")
                # Try to load from cache if available
                if os.path.exists(todoist_calendar_pickle):
                    logging.info("Loading from stale cache due to error")
                    with open(todoist_calendar_pickle, 'rb') as cal:
                        calendar_events = pickle.load(cal)
                else:
                    raise

        else:
            logging.info("Found in cache")
            with open(todoist_calendar_pickle, 'rb') as cal:
                calendar_events = pickle.load(cal)

        if len(calendar_events) == 0:
            logging.info("No upcoming tasks found.")

        return calendar_events
