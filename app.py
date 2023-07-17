import os
import sys
import base64
import atexit
import subprocess
import numpy as np
from PIL import Image
from io import BytesIO
from signal import SIGINT
from threading import Lock
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

sys.path.append(os.getcwd()+"/rpi-rgb-led-matrix/bindings/python")
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from modules import clock

app = Flask(__name__)

async_mode = 'threading'
socketio = SocketIO(app, async_mode=async_mode, max_http_bufffer_size=100000)
thread = None
thread_lock = Lock()

display_on = True
current_module = 'clock'
brightness = 50
theme = 'hk2'
proc = None

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.gpio_slowdown = 4
options.brightness = 50
options.pwm_lsb_nanoseconds = 130
options.limit_refresh_rate_hz = 0
options.led_rgb_sequence = 'RBG'
options.hardware_mapping = 'adafruit-hat-pwm'
options.drop_privileges = False

matrix = None
canvas = None

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
    global proc, display_on, brightness, theme, matrix, canvas
    if display_on:
        if proc:
            subprocess.run(['sudo', 'kill', str(os.getpgid(proc.pid))], check=False)
            proc = None
            display_on = False
        else:
            matrix = None
            canvas = None
            run_clock()
    else:
        run_clock()
        display_on = True

@socketio.on('theme_update')
def set_theme(data):
    global theme
    theme = data['value']
    if display_on:
        display_off()
        run_clock()

@socketio.on('brightness_update')
def set_brightness(data):
    global brightness, display_on
    brightness = data['value']
    if not display_on:
        return
    if brightness == '0':
        display_off()
    else:
        display_off()
        run_clock()

@socketio.on('grid_send')
def show_grid(data):
    global display_on, matrix, canvas, proc, display_on
    display_on = True
    if proc or not matrix:
        display_off()
        matrix = RGBMatrix(options = options)
        canvas = matrix.CreateFrameCanvas()
    grid = data['value']
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            grid[i][j] = tuple(value[4:-1].split(','))
    array = np.array(grid, dtype=np.uint8)
    image = Image.fromarray(array)
    canvas.SetImage(image, unsafe=False)
    canvas = matrix.SwapOnVSync(canvas)

@socketio.on('grid_toggle')
def toggle_grid(data):
    global display_on, proc, canvas, matrix
    if display_on and proc:
            subprocess.run(['sudo', 'kill', str(os.getpgid(proc.pid))], check=False)
            proc = None
    if not matrix:
        matrix = RGBMatrix(options = options)
        canvas = matrix.CreateFrameCanvas()

def display_off():
    global proc, display_on, matrix, canvas
    if proc:
        subprocess.run(['sudo', 'kill', str(os.getpgid(proc.pid))], check=False)
        proc = None
    else:
        matrix = None
        canvas = None
    display_on = False

def run_clock():
    global proc, theme, brightness, display_on
    proc = subprocess.Popen(['sudo', '.venv/bin/python3', 'modules/clock.py', '-b', str(brightness), '-t', theme], preexec_fn=os.setpgrp)
    display_on = True

def handle_shutdown():
    global proc
    if proc:
        subprocess.run(['sudo', 'kill', str(os.getpgid(proc.pid))], check=False)

if __name__ == '__main__':
    atexit.register(handle_shutdown)
    run_clock()
    socketio.run(app, debug=False, host='0.0.0.0', port=5000)

