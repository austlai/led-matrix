import os
import base64
import atexit
import subprocess
from signal import SIGINT
from io import BytesIO
from threading import Lock
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from modules import clock

app = Flask(__name__)

async_mode = 'threading'
socketio = SocketIO(app, async_mode=async_mode, max_http_bufffer_size=100000)
thread = None
thread_lock = Lock()

proc = None
display_on = True
current_module = 'clock'
brightness = 50
theme = 'hk2'
modules = {
    'clock': ['sudo', '.venv/bin/python3', 'modules/clock.py', '-b', str(brightness), '-t', theme]
}

def panel_update():
    pass
    #while True:
        #socketio.sleep(1)
        #img = get_frame()
        #buffered = BytesIO()
        #img.save(buffered, format="png")
        #img_str = base64.b64encode(buffered.getvalue())
        #socketio.emit('panel_update', {'frame': img_str})

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('connect')
def connect():
    socketio.emit('init', { 'brightness': brightness, 'theme': theme })
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(panel_update)
            pass

@socketio.on('display_toggle')
def toggle_display(data):
    global proc, display_on, brightness, theme
    if display_on:
        subprocess.check_output(['sudo', 'kill', str(os.getpgid(proc.pid))])
    else:
        proc = subprocess.Popen(modules[current_module], preexec_fn=os.setpgrp)
    display_on = not display_on

@socketio.on('theme_update')
def set_theme(data):
    global theme
    theme = data['value']
    if display_on:
        refresh_display()

@socketio.on('brightness_update')
def set_brightness(data):
    global brightness, display_on
    brightness = data['value']
    if not display_on:
        return
    if brightness == '0':
        display_off()
    else:
        refresh_display()

def refresh_display():
    global proc, display_on, brightness, theme
    if display_on:
        subprocess.check_output(['sudo', 'kill', str(os.getpgid(proc.pid))])
    proc = subprocess.Popen(modules[current_module], preexec_fn=os.setpgrp)
    display_on = True

def display_off():
    global proc, display_on
    if display_on:
        subprocess.check_output(['sudo', 'kill', str(os.getpgid(proc.pid))])
    display_on = False

def handle_shutdown():
    global proc
    if proc:
        subprocess.check_output(['sudo', 'kill', str(os.getpgid(proc.pid))])

if __name__ == '__main__':
    atexit.register(handle_shutdown)
    proc = subprocess.Popen(modules[current_module], preexec_fn=os.setpgrp)
    socketio.run(app, debug=False, host='0.0.0.0', port=5000)

