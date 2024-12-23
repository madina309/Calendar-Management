from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Calendar Event class (OOP principles)
class CalendarEvent:
    def __init__(self, title, description, start_time, end_time):
        self.title = title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        """Convert the CalendarEvent object to dictionary to return as JSON"""
        return {
            'title': self.title,
            'description': self.description,
            'start_time': self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time': self.end_time.strftime("%Y-%m-%d %H:%M:%S")
        }

# Store events in memory (for simplicity)
events = [] 

# Endpoint to create a new event
@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()

    # Validate data
    if 'title' not in data or 'description' not in data or 'start_time' not in data or 'end_time' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        start_time = datetime.strptime(data['start_time'], "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(data['end_time'], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD HH:MM:SS'}), 400

    new_event = CalendarEvent(data['title'], data['description'], start_time, end_time)
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201

# Endpoint to get all events
@app.route('/events', methods=['GET'])
def get_events():
    event_list = [event.to_dict() for event in events]
    return jsonify(event_list), 200

# Endpoint to get an event by its index
@app.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    if event_id < 0 or event_id >= len(events):
        return jsonify({'error': 'Event not found'}), 404
    return jsonify(events[event_id].to_dict()), 200

# Endpoint to update an event
@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    if event_id < 0 or event_id >= len(events):
        return jsonify({'error': 'Event not found'}), 404

    data = request.get_json()
    event = events[event_id]

    event.title = data.get('title', event.title)
    event.description = data.get('description', event.description)

    if 'start_time' in data:
        try:
            event.start_time = datetime.strptime(data['start_time'], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD HH:MM:SS'}), 400

    if 'end_time' in data:
        try:
            event.end_time = datetime.strptime(data['end_time'], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD HH:MM:SS'}), 400

    return jsonify(event.to_dict()), 200

# Endpoint to delete an event
@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    if event_id < 0 or event_id >= len(events):
        return jsonify({'error': 'Event not found'}), 404

    events.pop(event_id)
    return jsonify({'message': 'Event deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)

