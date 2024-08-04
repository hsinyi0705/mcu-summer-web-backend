from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit  
import datetime
import json
from myUtil import pp

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*") # 初始化 Flask-SocketIO

CORS(app)


JSON_FILE = 'temi.json'

# def pp(message):
#     print(message)

pp("Server Start")

def load_data():
    try:
        with open(JSON_FILE, 'r') as file:
            data = json.load(file)
            if not data or "_default" not in data:
                data = {"_default": {}}
            return data
    except FileNotFoundError:
        return {"_default": {}}

def save_data(data):
    with open(JSON_FILE, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {'message': 'This is a test message from Flask'}
    return jsonify(data)

@app.route('/api/button-click', methods=['POST'])
def button_click():
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_addr = request.remote_addr
    print(f"[{t}] - [{ip_addr}] - receive a request")
    return jsonify({'status': 'success', 'timestamp': t})

@app.route('/api/locations', methods=['GET'])
def get_locations():
    data = load_data()
    locations = list(data["_default"].keys())
    return jsonify({"locations": locations})

def handle_add_location(args):
    data = load_data()
    data["_default"][args] = {
        'id': '',
        'ip': '',
        'selected_function': 'addLocation',
        'location': args
    }
    save_data(data)
    return {'status': 'added', 'command': 'addLocation', 'location': args}

def handle_go_to_location(args):
    data = load_data()
    if args in data["_default"]:
        return {'status': 'navigating', 'command': 'goToLocation', 'location': args}
    else:
        return {'status': 'not found', 'command': 'goToLocation', 'location': args}

def handle_delete_location(args):
    data = load_data()
    if args in data["_default"]:
        del data["_default"][args]
        save_data(data)
        return {'status': 'deleted', 'command': 'deleteLocation', 'location': args}
    else:
        return {'status': 'not found', 'command': 'deleteLocation', 'location': args}

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@socketio.on('command')
def handle_command(data):
    command = data.get('command')
    args = data.get('args')
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{t}] - [COMMAND] - Received command: {command} with args: {args}")
    
    response = {'status': 'unknown command', 'command': command}
    
    if command == 'addLocation':
        response = handle_add_location(args)
    elif command == 'goToLocation':
        response = handle_go_to_location(args)
    elif command == 'deleteLocation':
        response = handle_delete_location(args)
    
    emit('response', response)

if __name__ == '__main__':
    socketio.run(app, debug=False, port=5000)
