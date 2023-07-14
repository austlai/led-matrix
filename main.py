import sys
import os
import time
import configparser
from PIL import Image

from panels import default
from modules import timedate

def main():
    brightness = 50
    displayOn = True

    config = configparser.ConfigParser()
    parsed_configs = config.read('config')
    if len(parsed_configs) == 0:
        print("no config file found")
        sys.exit()

    canvas_width = 64
    canvas_height = 32

    empty = Image.new("RGB", (canvas_width, canvas_height), (0,0,0))

    modules = {
        'timedate': timedate.TimeDate(config),
        'weather' : WeatherModule(config),
        'spotify' : SpotifyModule(config),
        'train': Train(config),
        'video': Video(config),
        'gif': Gif(config)
    }

    app_list = [default.Default(config, modules),
                notion_v2.NotionScreen(config, modules),
                weather.WeatherScreen(config, modules),
                gif_viewer.GifScreen(config, modules),
                spotify_player.SpotifyScreen(config, modules)]

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
    options.limit_refresh_rate_hz = 150
    options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'
    options.drop_privileges = False
    matrix = RGBMatrix(options = options)

    while(True):
        frame = app_list[0].generate()
        if not displayOn:
            frame = empty

        #matrix.brightness = 100
        matrix.SetImage(frame)
        time.sleep(0.05)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted with Ctrl-C')
        sys.exit(0)
