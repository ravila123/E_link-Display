#!/usr/bin/python3
import datetime
import logging
import os

from calendar_providers.base_provider import BaseCalendarProvider, CalendarEvent
import requests


class TodoistCalendar(BaseCalendarProvider):
    """
    A lightweight "calendar-like" provider that pulls tasks from Todoist
    and exposes them as CalendarEvent objects for the rest of the code.
    No caching – every call fetches fresh data so cron updates always show
    the latest tasks.
    """

    def __init__(self, todoist_api_token, max_event_results, from_date, to_date):
        self.todoist_api_token = todoist_api_token
        self.max_event_results = max_event_results
        self.from_date = from_date
        self.to_date = to_date

    def get_calendar_events(self) -> list[CalendarEvent]:
        calendar_events: list[CalendarEvent] = []

        if not self.todoist_api_token:
            logging.error("Todoist API token not set. Set TODOIST_API_TOKEN in env.sh")
            return calendar_events

        logging.debug("Fetching tasks from Todoist (no cache)")

        try:
            headers = {
                "Authorization": f"Bearer {self.todoist_api_token}"
            }

            # Get all active tasks
            response = requests.get(
                "https://api.todoist.com/rest/v2/tasks",
                headers=headers,
                timeout=10,
            )
            response.raise_for_status()
            tasks = response.json()

            logging.debug(f"Fetched {len(tasks)} tasks from Todoist")

            for task in tasks:
                summary = task.get("content", "Untitled Task")

                # Only include tasks that have a due date
                due = task.get("due")
                if not due:
                    logging.debug(f"Skipping task without due date: {summary}")
                    continue

                due_date_str = due.get("date")
                due_datetime = due.get("datetime")

                # Convert Todoist due fields into Python date/datetime
                is_all_day = False

                if due_datetime:
                    # Example: "2025-11-20T18:30:00Z"
                    start = datetime.datetime.fromisoformat(
                        due_datetime.replace("Z", "+00:00")
                    )
                    end = start + datetime.timedelta(hours=1)
                elif due_date_str:
                    # All–day task
                    start = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
                    end = start
                    is_all_day = True
                else:
                    # No usable date object
                    continue

                # Optional: respect from_date / to_date if provided
                try:
                    if isinstance(self.from_date, datetime.date):
                        # Normalize event start to datetime for comparison
                        if isinstance(start, datetime.date) and not isinstance(start, datetime.datetime):
                            start_cmp = datetime.datetime.combine(start, datetime.time.min)
                        else:
                            start_cmp = start

                        from_cmp = (
                            datetime.datetime.combine(self.from_date, datetime.time.min)
                            if isinstance(self.from_date, datetime.date) and not isinstance(self.from_date, datetime.datetime)
                            else self.from_date
                        )
                        to_cmp = (
                            datetime.datetime.combine(self.to_date, datetime.time.max)
                            if isinstance(self.to_date, datetime.date) and not isinstance(self.to_date, datetime.datetime)
                            else self.to_date
                        )

                        logging.debug(f"Task '{summary}': start={start_cmp}, from={from_cmp}, to={to_cmp}")
                        
                        if start_cmp < from_cmp or start_cmp > to_cmp:
                            # Outside desired window
                            logging.debug(f"Task '{summary}' outside date range, skipping")
                            continue
                except Exception as e:
                    logging.debug(f"Date range filtering error (ignored): {e}")

                # Add priority emoji
                priority = task.get("priority", 1)
                if priority == 4:
                    summary = "🔴 " + summary  # P1
                elif priority == 3:
                    summary = "🟡 " + summary  # P2
                elif priority == 2:
                    summary = "🔵 " + summary  # P3

                calendar_events.append(
                    CalendarEvent(summary, start, end, is_all_day)
                )

                if len(calendar_events) >= self.max_event_results:
                    break

            # Sort by start time / date
            def sort_key(event: CalendarEvent):
                if event.start is None:
                    return datetime.datetime.max
                if isinstance(event.start, datetime.date) and not isinstance(
                    event.start, datetime.datetime
                ):
                    return datetime.datetime.combine(event.start, datetime.time.min)
                return event.start

            calendar_events.sort(key=sort_key)

        except Exception as e:
            logging.error(f"Error fetching Todoist tasks: {e}")

        if len(calendar_events) == 0:
            logging.info("No upcoming Todoist tasks found.")

        return calendar_events