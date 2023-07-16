import sys
import os
import time
import configparser
from PIL import Image
import datetime as dt

from panels import default
sys.path.append(os.getcwd()+"/rpi-rgb-led-matrix/bindings/python")
from rgbmatrix import RGBMatrix, RGBMatrixOptions

class Controller:
    def __init__(self, config):
        self.width = 64
        self.height = 32
        self.display_on = False
        self.brightness = 50
        self.empty = Image.new("RGB", (self.width, self.height), (0,0,0))

        self.modules = {
            # 'weather' : WeatherModule(config),
            # 'spotify' : SpotifyModule(config),
            # 'train': Train(config),
            # 'video': Video(config),
            # 'gif': Gif(config)
        }

        self.app_list = [default.Default(config),
            # weather.Weather(config, modules),
            # viewer.Gif(config, modules),
            # player.Spotify(config, modules)
        ]

        options = RGBMatrixOptions()
        options.rows = self.height
        options.cols = self.width
        options.gpio_slowdown = 4
        options.brightness = self.brightness
        options.pwm_lsb_nanoseconds = 130
        options.limit_refresh_rate_hz = 0
        options.led_rgb_sequence = 'RBG'
        options.hardware_mapping = 'adafruit-hat-pwm'  # If you have an Adafruit HAT: 'adafruit-hat'
        options.drop_privileges = False
        self.options = options

        self.matrix = RGBMatrix(options = self.options)
        
    def run(self):
        while(True):
            if dt.datetime.now().time() > dt.time(8, 0) and dt.datetime.now().time() <= dt.time(23, 59):
                self.display_on = True
            else:
                self.display_on = False

            if not self.display_on:
                frame = self.empty
            else:
                frame = self.app_list[0].generate()

            self.matrix.SetImage(frame, unsafe=False)
            time.sleep(0.5)

    def toggle_display(self):
        self.display_on = not self.display_on
        print(self.display_on)

if __name__ == '__main__':
    try:
        config = configparser.ConfigParser()
        parsed_configs = config.read('config')
        if len(parsed_configs) == 0:
            print("no config file found")
            sys.exit()
        run(config)
    except KeyboardInterrupt:
        print('Interrupted with Ctrl-C')
        sys.exit(0)
