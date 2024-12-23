from flask import Blueprint, jsonify, request
from app.services.calendar_service import CalendarService

# Initialize the service
calendar_service = CalendarService()

# Create a Blueprint for calendar-related routes
calendar_blueprint = Blueprint('calendar', __name__)

# Route to create a new calendar
@calendar_blueprint.route('/calendars', methods=['POST'])
def create_calendar():
    data = request.get_json()
    
    # Ensure 'name' is provided in the request body
    name = data.get('name')
    if not name:
        return jsonify({"error": "Calendar name is required"}), 400
    
    # Create the calendar using the service
    calendar = calendar_service.create_calendar(name)
    
    # Return the created calendar's information as a response
    return jsonify({
        "calendar_id": calendar.calendar_id,
        "name": calendar.name
    }), 201

# Route to get a calendar by its ID
@calendar_blueprint.route('/calendars/<int:calendar_id>', methods=['GET'])
def get_calendar(calendar_id):
    calendar = calendar_service.get_calendar(calendar_id)
    
    # If the calendar doesn't exist, return a 404 error
    if not calendar:
        return jsonify({"error": "Calendar not found"}), 404
    
    # Return the calendar's information
    return jsonify({
        "calendar_id": calendar.calendar_id,
        "name": calendar.name
    })

# Route to delete a calendar by its ID
@calendar_blueprint.route('/calendars/<int:calendar_id>', methods=['DELETE'])
def delete_calendar(calendar_id):
    calendar = calendar_service.get_calendar(calendar_id)
    
    # If the calendar doesn't exist, return a 404 error
    if not calendar:
        return jsonify({"error": "Calendar not found"}), 404
    
    # Delete the calendar using the service
    calendar_service.delete_calendar(calendar_id)
    
    # Return a success message
    return jsonify({"message": "Calendar deleted successfully"}), 204
