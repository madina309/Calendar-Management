class Event:
    def __init__(self, event_id, title, start_time, end_time):
        self.event_id = event_id
        self.title = title
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        """Converts the event object to a dictionary for JSON serialization."""
        return {
            "event_id": self.event_id,
            "title": self.title,
            "start_time": self.start_time,
            "end_time": self.end_time
        }
