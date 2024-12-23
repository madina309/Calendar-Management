
   

           from flask import Flask, jsonify, request, abort
from models import db, User, Calendar, Event
from datetime import datetime
import os

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendar.db'  # You can change to another DB like PostgreSQL or MySQL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')  # Use .env for sensitive keys

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

# Create a user (For demonstration purposes)
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if 'username' not in data or 'email' not in data:
        abort(400, description="Username and email are required.")
    
    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": "User created successfully", "user_id": user.id}), 201

# Create a calendar for a user
@app.route('/users/<int:user_id>/calendars', methods=['POST'])
def create_calendar(user_id):
    data = request.get_json()
    if 'name' not in data:
        abort(400, description="Calendar name is required.")
    
    user = User.query.get_or_404(user_id)
    calendar = Calendar(name=data['name'], user_id=user.id)
    db.session.add(calendar)
    db.session.commit()

    return jsonify({"message": "Calendar created successfully", "calendar_id": calendar.id}), 201

# Create an event for a calendar
@app.route('/calendars/<int:calendar_id>/events', methods=['POST'])
def create_event(calendar_id):
    data = request.get_json()
    if 'title' not in data or 'start_time' not in data or 'end_time' not in data:
        abort(400, description="Title, start_time, and end_time are required.")
    
    calendar = Calendar.query.get_or_404(calendar_id)
    start_time = datetime.strptime(data['start_time'], "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(data['end_time'], "%Y-%m-%d %H:%M:%S")
    
    event = Event(title=data['title'], description=data.get('description', ''), 
                  start_time=start_time, end_time=end_time, calendar_id=calendar.id)
    db.session.add(event)
    db.session.commit()

    return jsonify({"message": "Event created successfully", "event_id": event.id}), 201

# Get all events for a calendar
@app.route('/calendars/<int:calendar_id>/events', methods=['GET'])
def get_events(calendar_id):
    calendar = Calendar.query.get_or_404(calendar_id)
    events = Event.query.filter_by(calendar_id=calendar.id).all()
    event_list = [{"id": event.id, "title": event.title, "start_time": event.start_time, "end_time": event.end_time}
                  for event in events]

    return jsonify({"events": event_list})

if __name__ == "__main__":
    app.run(debug=True)
