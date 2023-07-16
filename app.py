import sys
import base64
import configparser
from io import BytesIO
from threading import Lock
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import controller
from panels import default

async_mode = 'threading'

app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode, max_http_bufffer_size=100000)
thread = None
thread_lock = Lock()

config = configparser.ConfigParser()
parsed_configs = config.read('config')
if len(parsed_configs) == 0:
    print("no config file found")
    sys.exit()

def panel_update():
    """Example of how to send server generated events to clients."""
    while True:
        socketio.sleep(1)
        img = default.Default(config).generate()
        buffered = BytesIO()
        img.save(buffered, format="png")
        img_str = base64.b64encode(buffered.getvalue())
        socketio.emit('panel_update', {'frame': img_str})

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('connect')
def connect():
    socketio.emit('init', { 'value': 50 })
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(panel_update)

@socketio.on('brightness_update')
def brightness(data):
    print(data['value'])

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
