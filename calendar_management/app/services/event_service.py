from app.models.event import Event
from app.models.calendar import Calendar

class EventService:
    def __init__(self, calendar_service):
        self.calendar_service = calendar_service  # Reference to the CalendarService instance

    def create_event(self, calendar_id, title, start_time, end_time):
        """Creates a new event and adds it to the specified calendar."""
        # Generate a new event_id (you could use UUID or another approach here)
        event_id = self._generate_event_id(calendar_id)
        event = Event(event_id=event_id, title=title, start_time=start_time, end_time=end_time)

        # Add the event to the calendar
        self.calendar_service.add_event_to_calendar(calendar_id, event)

        return event

    def update_event(self, calendar_id, event_id, title=None, start_time=None, end_time=None):
        """Updates an existing event on the specified calendar."""
        calendar = self.calendar_service.get_calendar(calendar_id)
        if not calendar:
            raise ValueError(f"Calendar with ID {calendar_id} not found")

        # Find the event in the calendar
        event = next((e for e in calendar.events if e.event_id == event_id), None)
        if not event:
            raise ValueError(f"Event with ID {event_id} not found")

        # Update event fields
        if title:
            event.title = title
        if start_time:
            event.start_time = start_time
        if end_time:
            event.end_time = end_time

        return event

    def delete_event(self, calendar_id, event_id):
        """Deletes an event from the specified calendar."""
        try:
            self.calendar_service.remove_event_from_calendar(calendar_id, event_id)
            return f"Event {event_id} removed successfully"
        except ValueError:
            raise ValueError(f"Event with ID {event_id} not found in calendar {calendar_id}")

    def get_event(self, calendar_id, event_id):
        """Retrieves a specific event from a calendar by its ID."""
        calendar = self.calendar_service.get_calendar(calendar_id)
        if not calendar:
            raise ValueError(f"Calendar with ID {calendar_id} not found")

        event = next((e for e in calendar.events if e.event_id == event_id), None)
        if not event:
            raise ValueError(f"Event with ID {event_id} not found")

        return event

    def _generate_event_id(self, calendar_id):
        """Generates a unique event ID (for simplicity, use the number of events in the calendar)."""
        calendar = self.calendar_service.get_calendar(calendar_id)
        if not calendar:
            raise ValueError(f"Calendar with ID {calendar_id} not found")
        
        return len(calendar.events) + 1  # This could be improved with more robust ID generation (e.g., UUID)
