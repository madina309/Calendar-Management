from app.models.calendar import Calendar
from app.models.event import Event

class CalendarService:
    def __init__(self):
        # In-memory store of calendars, where key is the calendar_id
        self.calendars = {}

    def create_calendar(self, name):
        """Creates a new calendar and adds it to the store."""
        # Generate a new calendar_id (you could use UUID or a more robust approach here)
        calendar_id = len(self.calendars) + 1
        calendar = Calendar(calendar_id=calendar_id, name=name)
        self.calendars[calendar_id] = calendar
        return calendar

    def get_calendar(self, calendar_id):
        """Retrieves a calendar by its ID."""
        return self.calendars.get(calendar_id)

    def delete_calendar(self, calendar_id):
        """Deletes a calendar by its ID."""
        if calendar_id in self.calendars:
            del self.calendars[calendar_id]
        else:
            raise ValueError(f"Calendar with ID {calendar_id} not found")

    def add_event_to_calendar(self, calendar_id, event):
        """Adds an event to the specified calendar."""
        calendar = self.get_calendar(calendar_id)
        if calendar:
            calendar.add_event(event)
        else:
            raise ValueError(f"Calendar with ID {calendar_id} not found")

    def remove_event_from_calendar(self, calendar_id, event_id):
        """Removes an event from the specified calendar."""
        calendar = self.get_calendar(calendar_id)
        if calendar:
            event = next((e for e in calendar.events if e.event_id == event_id), None)
            if event:
                calendar.remove_event(event)
            else:
                raise ValueError(f"Event with ID {event_id} not found")
        else:
            raise ValueError(f"Calendar with ID {calendar_id} not found")
