import base64
import subprocess
from signal import SIGINT
from io import BytesIO
from threading import Lock
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from modules import clock

async_mode = 'threading'

app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode, max_http_bufffer_size=100000)
thread = None
thread_lock = Lock()
display_on = False
current_module = 0
modules = {
    'clock': ['sudo', '.venv/bin/python3', 'modules/clock.py']
}

def panel_update():
    """Example of how to send server generated events to clients."""
    clock_module = clock.Clock(50, 'hk2')
    while True:
        socketio.sleep(1)
        img = clock_module.get_frame()
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

@socketio.on('display_toggle')
def display_toggle():
    global proc
    if display_on and proc:
        proc.send_signal(SIGINT)
    else:
        proc = subprocess.Popen(['sudo', '.venv/bin/python3', 'modules/clock.py'])

@socketio.on('brightness_update')
def brightness(data):
    print(data['value'])

if __name__ == '__main__':
    proc = subprocess.Popen(['sudo', '.venv/bin/python3', 'modules/clock.py'])
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

