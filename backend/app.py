import os
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__, static_folder='../frontend/build', static_url_path='')
# Allow requests from the frontend running on localhost:3000
CORS(app, origins=["http://localhost:3000"])

# Connect to MongoDB running on localhost:27017
client = MongoClient("mongodb://localhost:27017/")
db = client['ai_scheduling_app']  # Database name
tasks_collection = db['tasks']    # Collection to store tasks

def plan_day(tasks):
    # Simulate processing delay (replace with an actual LLM integration)
    time.sleep(3)
    # Dummy scheduling logic (replace with smart scheduling)
    schedule = [
        {"time": "11AM", "task": "Prepare for meeting with Jessica at work", "reason": "Critical meeting preparation"},
        {"time": "1PM", "task": "Go for a 20 minute run", "reason": "Wellness break"},
        {"time": "2PM", "task": "Mow the lawn", "reason": "Bundled outdoor activities"},
        {"time": "4PM", "task": "Help daughter with Science project", "reason": "Non-skippable family commitment"}
    ]
    return schedule

@app.route('/plan', methods=['POST'])
def plan():
    data = request.get_json()
    tasks = data.get('tasks', [])
    
    # Save the tasks to MongoDB
    task_doc = {"tasks": tasks}
    tasks_collection.insert_one(task_doc)
    
    schedule = plan_day(tasks)
    return jsonify(schedule)

# Serve the React app's static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)

