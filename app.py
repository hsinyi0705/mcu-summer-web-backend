from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit  # 确保这行代码存在

from myUtil import pp
import datetime


app = Flask(__name__)
# 初始化 Flask-SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

locations = {}

pp('Server Start')

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

    if command == 'addLocation':
        locations[args] = {'name': args}
        emit('response', {'status': 'added', 'command': command, 'location': args})
    elif command == 'goToLocation':
        if args in locations:
            emit('response', {'status': 'navigating', 'command': command, 'location': args})
        else:
            emit('response', {'status': 'not found', 'command': command, 'location': args})
    elif command == 'deleteLocation':
        if args in locations:
            del locations[args]
            emit('response', {'status': 'deleted', 'command': command, 'location': args})
        else:
            emit('response', {'status': 'not found', 'command': command, 'location': args})
    else:
        emit('response', {'status': 'unknown command', 'command': command})
        
if __name__ == '__main__':
    socketio.run(app, debug=True)