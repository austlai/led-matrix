import sys
import os
import time
import configparser
from PIL import Image
import datetime as dt

from panels import default

def main():
    brightness = 50
    display_on = True

    config = configparser.ConfigParser()
    parsed_configs = config.read('config')
    if len(parsed_configs) == 0:
        print("no config file found")
        sys.exit()

    canvas_width = 64
    canvas_height = 32

    empty = Image.new("RGB", (canvas_width, canvas_height), (0,0,0))

    modules = {
        # 'weather' : WeatherModule(config),
        # 'spotify' : SpotifyModule(config),
        # 'train': Train(config),
        # 'video': Video(config),
        # 'gif': Gif(config)
    }

    app_list = [default.Default(config),
        # weather.Weather(config, modules),
        # viewer.Gif(config, modules),
        # player.Spotify(config, modules)
    ]

    currentdir = os.getcwd()
    sys.path.append(currentdir+"/rpi-rgb-led-matrix/bindings/python")
    print(currentdir)
    from rgbmatrix import RGBMatrix, RGBMatrixOptions

    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.brightness = brightness
    options.gpio_slowdown = 4
    options.pwm_lsb_nanoseconds = 130
    options.limit_refresh_rate_hz = 200
    options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'
    options.drop_privileges = False
    matrix = RGBMatrix(options = options)

    while(True):
        if dt.datetime.now().time() > dt.time(8, 0) and dt.datetime.now().time() <= dt.time(23, 59):
            display_on = True
        else:
            display_on = False

        frame = app_list[0].generate()
        if not display_on:
            frame = empty

        matrix.SetImage(frame)
        time.sleep(0.5)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted with Ctrl-C')
        sys.exit(0)
