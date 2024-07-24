from flask import Flask, jsonify, request
from flask_cors import CORS
from myUtil import pp
import datetime


app = Flask(__name__)

CORS(app)

pp('Server Start')

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {'message': 'This is a test message from Flask'}
    return jsonify(data)

@app.route('/api/button-click', methods=['POST', 'GET'])
def button_click():
    t=str(datetime.datetime.now().year)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().day)+" "+str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)
    print(f"receive a request from {request.remote_addr} at {t}")
    return jsonify({'status': 'success', 'timestamp': t})


if __name__ == '__main__':
    app.run(debug=True)
