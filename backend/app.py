import os
import time
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='../frontend/build', static_url_path='')

def plan_day(tasks):
    # Simulate processing delay (replace with LLM integration)
    time.sleep(3)
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
    schedule = plan_day(tasks)
    return jsonify(schedule)

# Serve the React app
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
