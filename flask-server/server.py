from glasses import FrontendData

from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import threading

import sqlite3

app = Flask(__name__)

CORS(app, origins=["http://localhost:3000"])

# States
NOT_STARTED = 0
WORK_RUNNING = 1
WORK_PAUSED = 2
REST_RUNNING = 3
REST_PAUSED = 4

state = NOT_STARTED
WORK_BLOCK = 11   # 10 minutes in seconds
REST_BLOCK = 21  # 20 minutes in seconds

end_time = None
remaining_time_when_paused = None
frontend = None
gazeValues = None
pupilValue = None

def init_db():
    conn = sqlite3.connect("eye_focus.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS EyeDistanceData (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        User_ID INTEGER NOT NULL,
        Distance REAL NOT NULL,
        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

@app.route("/initdb", methods=["GET"])
def initdb():
    init_db()
    return "DB initialized"

@app.route("/insert_distance", methods=["POST"])
def insert_distance():
    data = request.json
    user_id = data.get("user_id")
    distance = data.get("distance")

    conn = sqlite3.connect("eye_focus.db")
    c = conn.cursor()
    c.execute("INSERT INTO EyeDistanceData (User_ID, Distance) VALUES (?, ?)", (user_id, distance))
    conn.commit()
    conn.close()

    return jsonify({"status": "Distance data inserted"})


@app.route("/get_distances", methods=["GET"])
def get_distances():
    conn = sqlite3.connect("eye_focus.db")
    c = conn.cursor()
    c.execute("SELECT * FROM EyeDistanceData")
    data = c.fetchall()
    conn.close()

    return jsonify(data)

@app.route('/control', methods=['POST'])
def control():
    global state, end_time, remaining_time_when_paused, frontend

    action = request.json.get("action")
    current_time = time.time()
    
    if action == "start":
        state = WORK_RUNNING
        end_time = current_time + WORK_BLOCK
        
        
    elif action == "pause":
        if state in [WORK_RUNNING, REST_RUNNING]:
            remaining_time_when_paused = end_time - current_time
            end_time = current_time  # Immediately update to reflect paused state
            state = WORK_PAUSED if state == WORK_RUNNING else REST_PAUSED
    elif action == "resume":
        if state in [WORK_PAUSED, REST_PAUSED]:
            state = WORK_RUNNING if state == WORK_PAUSED else REST_RUNNING
            end_time = current_time + remaining_time_when_paused

    return jsonify({"status": "ok"})

def record_data():
    while True:
        if frontend:
            print(frontend.eyeValues[2])
            distance = frontend.eyeValues[2]  # Assuming this method gives the distance you want to store
            user_id = 1  # You might want to change this based on your requirements

            conn = sqlite3.connect("eye_focus.db")
            c = conn.cursor()
            c.execute("INSERT INTO EyeDistanceData (User_ID, Distance) VALUES (?, ?)", (user_id, distance))
            conn.commit()
            conn.close()
        time.sleep(5)

@app.route('/connectToGlasses', methods=['POST'])
def connectToGlasses():
    global frontend
    frontend = FrontendData()

    # Start recording data in a separate thread
    t = threading.Thread(target=record_data)
    t.daemon = True  # This ensures the thread will be stopped when the application stops
    t.start()

    return jsonify({"status": "ok"})

@app.route('/disconnect', methods=['POST'])
def disconnect():
    global frontend
    frontend.shutdown()
    return jsonify({"status": "ok"})

@app.route('/time_left')
def time_left():
    global state, end_time, frontend, gazeValues, pupilValue
    current_time = time.time()

    print(frontend)
    if(frontend != None):
        print(frontend.getGazeValues())
        gazeValues = frontend.getGazeValues()
        pupilValue = frontend.getPupilValue()

    if state == NOT_STARTED:
        return jsonify({"time_left": 0, "state": state})
    
    # Handle the paused states
    if state in [WORK_PAUSED, REST_PAUSED]:
        return jsonify({"time_left": remaining_time_when_paused, "state": state, "gazeValues": gazeValues, "pupilValue": pupilValue})
    
    time_left = end_time - current_time

    if time_left < 0:
        if state in [WORK_RUNNING, REST_RUNNING]:  # Only reset if running
            time_left = 0
            state = REST_RUNNING if state == WORK_RUNNING else WORK_RUNNING
            end_time = current_time + (REST_BLOCK if state == REST_RUNNING else WORK_BLOCK)

    return jsonify({"time_left": time_left, "state": state, "gazeValues": gazeValues, "pupilValue": pupilValue})

@app.route('/reset', methods=['POST'])
def reset():
    global state, end_time, remaining_time_when_paused
    state = NOT_STARTED
    end_time = None
    remaining_time_when_paused = None
    return jsonify({"status": "reset"})


if __name__ == "__main__":
    app.run(debug=True)
