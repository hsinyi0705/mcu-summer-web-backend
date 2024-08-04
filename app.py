from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit  

from myUtil import pp
import datetime
import json


app = Flask(__name__)
# 初始化 Flask-SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# JSON 文件路径
JSON_FILE = 'temi.json'

# locations = {}

pp('Server Start')

def load_data():
    with open(JSON_FILE, 'r') as file:
        return json.load(file)

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
    t = str(datetime.datetime.now())
    # t=str(datetime.datetime.now().year)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().day)+" "+str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)
    print(f"receive a request from {request.remote_addr} at {t}")
    return jsonify({'status': 'success', 'timestamp': t})

@app.route('/api/locations', methods=['GET'])
def get_locations():
    data = load_data()
    print(data)  # 打印加载的 JSON 数据
    locations = list(data["_default"].keys())
    print(locations)  # 打印提取的地理位置列表
    return jsonify({"locations": locations})

# 处理 WebSocket 连接
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
    print(f"Received command: {command} with args: {args}")

    data = load_data()
    if command == 'addLocation':
        data["_default"][args] = {'name': args}
        save_data(data)
        emit('response', {'status': 'added', 'command': command, 'location': args})
    elif command == 'goToLocation':
        if args in data["_default"]:
            emit('response', {'status': 'navigating', 'command': command, 'location': args})
        else:
            emit('response', {'status': 'not found', 'command': command, 'location': args})
    elif command == 'deleteLocation':
        if args in data["_default"]:
            del data["_default"][args]
            save_data(data)
            emit('response', {'status': 'deleted', 'command': command, 'location': args})
        else:
            emit('response', {'status': 'not found', 'command': command, 'location': args})
    else:
        emit('response', {'status': 'unknown command', 'command': command})
        
if __name__ == '__main__':
    # socketio.run(app, debug=True)
    socketio.run(app, debug=True, port=5000)
