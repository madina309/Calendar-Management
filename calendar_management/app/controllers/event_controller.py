from flask import Blueprint, jsonify, request
from app.services.event_service import EventService
from app.services.calendar_service import CalendarService

# Initialize the service
calendar_service = CalendarService()
event_service = EventService()

# Create a Blueprint for event-related routes
event_blueprint = Blueprint('event', __name__)

# Route to create a new event in a specific calendar
@event_blueprint.route('/calendars/<int:calendar_id>/events', methods=['POST'])
def create_event(calendar_id):
    data = request.get_json()
    
    # Extract event details from the request body
    title = data.get('title')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    
    if not title or not start_time or not end_time:
        return jsonify({"error": "Title, start time, and end time are required"}), 400
    
    # Get the calendar from the service
    calendar = calendar_service.get_calendar(calendar_id)
    if not calendar:
        return jsonify({"error": "Calendar not found"}), 404

    # Create the event using the service
    event = event_service.create_event(calendar, title, start_time, end_time)
    
    # Return the created event's details
    return jsonify({
        "event_id": event.event_id,
        "title": event.title,
        "start_time": event.start_time,
        "end_time": event.end_time
    }), 201

# Route to get an event by its ID
@event_blueprint.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = event_service.get_event(event_id)
    
    # If the event doesn't exist, return a 404 error
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    # Return the event's details
    return jsonify({
        "event_id": event.event_id,
        "title": event.title,
        "start_time": event.start_time,
        "end_time": event.end_time
    })

# Route to delete an event by its ID
@event_blueprint.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = event_service.get_event(event_id)
    
    # If the event doesn't exist, return a 404 error
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    # Find the calendar containing the event
    for calendar in calendar_service.calendars.values():
        if event in calendar.events:
            # Delete the event using the service
            event_service.delete_event(calendar, event_id)
            return jsonify({"message": "Event deleted successfully"}), 204
    
    return jsonify({"error": "Event not found in any calendar"}), 404
