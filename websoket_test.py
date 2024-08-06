from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

socketio = SocketIO(app, cors_allowed_origins="*")  # 初始化 Flask-SocketIO


@app.route('/')
def index():
    return 'WebSocket Server is running!'

@socketio.on('command')
def handle_command(data):
    try:
        command = data.get('command')
        args = data.get('args')
        a_id = data.get('a_id')
        b_ip = data.get('b_ip')

        # 确保所有必要的字段都存在
        if command is None or args is None or a_id is None or b_ip is None:
            raise ValueError("Missing required fields")

        print(f'Received command: {command}')
        print(f'Args: {args}')  # 这里打印 args 参数
        print(f'a_id: {a_id}')
        print(f'b_ip: {b_ip}')

        # 处理命令的逻辑
        # ...
        
        emit('response', {'status': 'success', 'message': 'Command received'})
    except Exception as e:
        print(f'Error handling command: {e}')
        emit('response', {'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    socketio.run(app, debug=True)
