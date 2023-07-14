from threading import Lock
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import configparser
import base64
from io import BytesIO
from PIL import Image


from panels import default

async_mode = 'threading'

app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode, max_http_bufffer_size=100000)
thread = None
thread_lock = Lock()

brightness = 100
displayOn = True

config = configparser.ConfigParser()
parsed_configs = config.read('../config')
if len(parsed_configs) == 0:
    print("no config file found")
    # sys.exit()

canvas_width = 64
canvas_height = 32

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(3)
        count += 1
        img = default.Default(config).generate()
        buffered = BytesIO()
        img.save(buffered, format="png")
        img_str = base64.b64encode(buffered.getvalue())

        socketio.emit('background_resp', {'frame': img_str, 'count': count})

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('connect_resp', {'data': 'Connected', 'count': 0})

if __name__ == '__main__':
    socketio.run(app)
