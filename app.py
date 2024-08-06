# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from flask_socketio import SocketIO, emit  
# import datetime
# import json
# from myUtil import pp

# app = Flask(__name__)
# socketio = SocketIO(app, cors_allowed_origins="*") # 初始化 Flask-SocketIO

# CORS(app)


# JSON_FILE = 'temi.json'

# # def pp(message):
# #     print(message)

# pp("Server Start")

# def load_data():
#     try:
#         with open(JSON_FILE, 'r') as file:
#             data = json.load(file)
#             if not data or "_default" not in data:
#                 data = {"_default": {}}
#             return data
#     except FileNotFoundError:
#         return {"_default": {}}

# def save_data(data):
#     with open(JSON_FILE, 'w') as file:
#         json.dump(data, file, indent=4)


# @app.route('/')
# def index():
#     return "Hello, World!-"

# @app.route('/api/data', methods=['GET'])
# def get_data():
#     data = {'message': 'This is a test message from Flask'}
#     return jsonify(data)

# @app.route('/api/button-click', methods=['POST'])
# def button_click():
#     t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     ip_addr = request.remote_addr
#     print(f"[{t}] - [{ip_addr}] - receive a request")
#     return jsonify({'status': 'success', 'timestamp': t})

# @app.route('/api/locations', methods=['GET'])
# def get_locations():
#     data = load_data()
#     locations = list(data["_default"].keys())
#     return jsonify({"locations": locations})
# #從temi匯入資料
# def handle_add_location(args):
#     data = load_data()
#     data["_default"][args] = {
#         'id': '',
#         'ip': '',
#         'selected_function': 'addLocation',
#         'location': args
#     }
#     save_data(data)
#     return {'status': 'added', 'command': 'addLocation', 'location': args}
# #前往地點
# def handle_go_to_location(args):
#     data = load_data()
#     if args in data["_default"]:
#         return {'status': 'navigating', 'command': 'goToLocation', 'location': args}
#     else:
#         return {'status': 'not found', 'command': 'goToLocation', 'location': args}

# def handle_delete_location(args):
#     data = load_data()
#     if args in data["_default"]:
#         del data["_default"][args]
#         save_data(data)
#         return {'status': 'deleted', 'command': 'deleteLocation', 'location': args}
#     else:
#         return {'status': 'not found', 'command': 'deleteLocation', 'location': args}

# # @socketio.on('connect')
# # def handle_connect():
# #     print("Client connected")

# @socketio.on('connect')
# def handle_connect():
#     print("Client connected")
#     # # 假設你有機器人的 ID 和 IP
#     # robot_id = '12345'
#     # robot_ip = '192.168.1.102'
#     # print(f"Sending ID: {robot_id}, IP: {robot_ip}")
#     # emit('response', {'type': 'onConnect', 'id': robot_id, 'ip': robot_ip})

# @socketio.on('disconnect')
# def handle_disconnect():
#     print("Client disconnected")

# @socketio.on('command')
# def handle_command(data):
#     command = data.get('command')
#     args = data.get('args', {})
#     t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     print(f"[{t}] - [COMMAND] - Received command: {command} with args: {args}")

#     response = {'status': 'unknown command', 'command': command}
    
#     if command == 'addLocation':
#         response = handle_add_location(args)
#     elif command == 'goToLocation':
#         response = handle_go_to_location(args)
#     elif command == 'deleteLocation':
#         response = handle_delete_location(args)
    
#     print(f"[{t}] - [COMMAND RESPONSE] - Sending response: {response}")
#     emit('response', response)

# @socketio.on('response')
# def handle_response(data):
#     print(f"Received response data from robot: {data}")
#     robot_id = data.get('id')
#     robot_ip = data.get('ip')
#     print(f"Received ID: {robot_id}, IP: {robot_ip}")
#     emit('response', {'type': 'onConnect', 'id': robot_id, 'ip': robot_ip})

# if __name__ == '__main__':
#     socketio.run(app, debug=False, host='0.0.0.0', port=5000)
#------------------------
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit  
import datetime
import json
import socketio
from aiohttp import web

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # 初始化 Flask-SocketIO

CORS(app)

JSON_FILE = 'temi.json'

def load_data():
    try:
        with open(JSON_FILE, 'r') as file:
            data = json.load(file)
            if not data or "_default" not in data:
                data = {"_default": {}}
            return data
    except FileNotFoundError:
        return {"_default": {}}

def save_data(data):#2
    with open(JSON_FILE, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def index():
    return "Hello, World!-"

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

####################
####################

def handle_add_location(args):
    data = load_data()#0
    data["_default"][args] = {
        'id': '',
        'ip': '',
        'selected_function': 'addLocation',
        'location': args
    }
    save_data(data)#1
    return {'id' : a_id,"ip" : b_ip,'status': 'ADD', 'command': 'addLocation', 'location': args}

def handle_go_to_location(args):
    data = load_data()
    
    data["_default"][args] = {
        'id': '',
        'ip': '',
        'selected_function': 'goToLocation',
        'location': args
    }
    save_data(data)
    # if args in data["_default"]:
    return {'status': 'GO', 'command': 'goToLocation', 'location': args}
    # else:
    #     return {'status': 'not found', 'command': 'goToLocation', 'location': args}

def handle_delete_location(args):
    data = load_data()
    
    if args in data["_default"]:
        del data["_default"][args]
        save_data(data)
        return {'status': 'DELETE', 'command': 'deleteLocation', 'location': args}
    else:
        return {'status': 'not found', 'command': 'deleteLocation', 'location': args}

# def handle_speak(args):
#     data = load_data()
#     data["_default"][args] = {
#         'id': 'ddd',
#         'ip': '444',
#         'selected_function': 'speak',
#         'location': args
#     }
#     save_data(data)
#     return {'status': 'SPEAK', 'command': 'speak', 'location': args}

####################
####################

@socketio.on('connect')
def handle_connect():
    data = load_data()
    locations = list(data["_default"].keys())
    print(f"Client connected. Available locations: {locations}")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@socketio.on('command')
def handle_command(data):
    command = data.get('command')
    args = data.get('args', {})
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{t}] - [COMMAND] - Received command: {command} with args: {args}")

    response = {'status': 'unknown command', 'command': command}
    
    if command == 'onConnect':
        robot_id = 'id'
        robot_ip = 'ip'
        response = {'status': 'received', 'command': 'onConnect', 'id': robot_id, 'ip': robot_ip}
        print(f"Received ID: {robot_id}, IP: {robot_ip}")
    elif command == 'addLocation':
        response = handle_add_location(args)
    elif command == 'goToLocation':
        response = handle_go_to_location(args)
    elif command == 'deleteLocation':
        response = handle_delete_location(args)
    # elif command == 'speak':
    #     response = handle_speak(args)
    
    print(f"[{t}] - [COMMAND RESPONSE] - Sending response: {response}")
    emit('response', response)
#message

# @socketio.on('command')
# def handle_command(data):
#     command = data.get('command')
#     args = data.get('args', {})
#     t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     print(f"[{t}] - [COMMAND] - Received command: {command} with args: {args}")

#     message = {'status': 'unknown command', 'command': command}
    
#     if command == 'onConnect':
#         robot_id = data.get('id')
#         robot_ip = data.get('ip')
#         message = {'status': 'received', 'command': 'onConnect', 'id': robot_id, 'ip': robot_ip}
#         print(f"Received ID: {robot_id}, IP: {robot_ip}")
#     elif command == 'addLocation':
#         message = handle_add_location(args)
#     elif command == 'goToLocation':
#         message = handle_go_to_location(args)
#     elif command == 'deleteLocation':
#         message = handle_delete_location(args)
#     # elif command == 'speak':
#     #     message = handle_speak(args)
    
#     print(f"[{t}] - [COMMAND MESSAGE] - Sending message: {message}")
#     emit('message', message)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
