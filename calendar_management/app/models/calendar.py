class Calendar:
    def __init__(self, calendar_id, name):
        self.calendar_id = calendar_id
        self.name = name
        self.events = []  # List to hold events associated with this calendar

    def add_event(self, event):
        """Adds an event to the calendar's event list."""
        self.events.append(event)

    def remove_event(self, event):
        """Removes an event from the calendar's event list."""
        if event in self.events:
            self.events.remove(event)
    
    def to_dict(self):
        """Converts the calendar object to a dictionary."""
        return {
            "calendar_id": self.calendar_id,
            "name": self.name,
            "events": [event.to_dict() for event in self.events]  # Converts all events to dictionaries
        }
