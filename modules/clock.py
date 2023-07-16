import time
import sys
import os
import datetime as dt
from PIL import Image, ImageDraw, ImageFont

sys.path.append(os.getcwd()+"/rpi-rgb-led-matrix/bindings/python")
from rgbmatrix import RGBMatrix, RGBMatrixOptions

LIGHT_PINK = (255,219,218)
DARK_PINK = (219,127,142)
WHITE = (230,255,255)

SALMON = (255,150,162)
TAN = (255,205,178)
ORANGE_TINTED_WHITE = (248,237,235)

BLACK = (0, 0, 0)
DARK_RED = (46, 0, 51)

CYAN = (128, 247, 255)

THEMES = {
    'sakura' : {
        'image': 'res/sakura.png',
        'timepos': (3, 6),
        'date': True,
        'datepos': (23, 6),
        'primary': LIGHT_PINK,
        'secondary': DARK_PINK,
        'border': False,
    },
    'cat' : {
        'image': 'res/cat.jpg',
        'timepos': (3, 6),
        'date': True,
        'datepos': (23, 6),
        'primary': LIGHT_PINK,
        'secondary': DARK_PINK,
        'border': False,
    },
    'dm' : {
        'image': 'res/dm.jpg',
        'timepos': (45, 2),
        'date': True,
        'datepos': (45, 8),
        'primary': LIGHT_PINK,
        'secondary': DARK_PINK,
        'border': False,
    },
    'flowers' : {
        'image': 'res/flowers.jpg',
        'timepos': (3, 6),
        'date': True,
        'datepos': (23, 6),
        'primary': LIGHT_PINK,
        'secondary': DARK_PINK,
        'border': False,
    },
    'ponyo' : {
        'image': 'res/ponyo.jpg',
        'timepos': (4, 4),
        'date': False,
        'datepos': (4, 4),
        'primary': WHITE,
        'secondary': CYAN,
        'border': True,
    },
    'hk1' : {
        'image': 'res/hk1.png',
        'timepos': (3, 6),
        'date': True,
        'datepos': (23, 6),
        'primary': LIGHT_PINK,
        'secondary': DARK_PINK,
        'border': False,
    },
    'hk2' : {
        'image': 'res/hk2.png',
        'timepos': (3, 6),
        'date': True,
        'datepos': (23, 6),
        'primary': LIGHT_PINK,
        'secondary': DARK_PINK,
        'border': False,
    },
}

WIDTH = 64
HEIGHT = 32

class Clock:
    def __init__(self, brightness, theme) -> None:
        self.loop_time = 20
        self.show_day = True
        self.update_time = None
        self.theme = theme
        self.empty = Image.new("RGB", (WIDTH, HEIGHT), (0,0,0))

        options = RGBMatrixOptions()
        options.rows = HEIGHT
        options.cols = WIDTH
        options.gpio_slowdown = 4
        options.brightness = brightness
        options.pwm_lsb_nanoseconds = 130
        options.limit_refresh_rate_hz = 0
        options.led_rgb_sequence = 'RBG'
        options.hardware_mapping = 'adafruit-hat-pwm'
        options.drop_privileges = False

        self.matrix = RGBMatrix(options = options)

    def run(self):
        while(True):
            if dt.datetime.now().time() > dt.time(8, 0) and dt.datetime.now().time() <= dt.time(23, 59):
                frame = self.get_frame()
            else:
                frame = self.empty

            self.matrix.SetImage(frame)
            time.sleep(0.5)

    def get_frame(self):
        if (self.update_time is None):
            self.update_time = time.time()
        if (time.time() - self.update_time >= self.loop_time):
            self.show_day = not self.show_day
            self.update_time = time.time()

        theme = THEMES[self.theme]
        frame = Image.open(theme['image']).convert("RGB")

        self.set_datetime(frame, theme, self.show_day)

        return frame

    def set_datetime(self, frame, theme, show_day):
        now = dt.datetime.now()
        dayOfWeek = now.strftime("%A")[:3].upper()

        font = ImageFont.truetype("fonts/tiny.otf", 5)
        draw = ImageDraw.Draw(frame)

        tpos = theme['timepos']
        dpos = theme['datepos']

        if (theme['border']):
            draw.rectangle(((tpos[0] - 2, tpos[1] - 2), (tpos[0] + 18, tpos[1] + 6)), BLACK)

        draw.text(tpos, padNum(now.hour), theme['primary'], font=font)
        draw.text((tpos[0] + 7, tpos[1]), ":", theme['primary'], font=font)
        draw.text((tpos[0] + 10, tpos[1]), padNum(now.minute), theme['primary'], font=font)

        if theme['date']:
            if show_day:
                if theme['border']:
                    draw.rectangle(((dpos[0] - 2, dpos[1] - 2), (dpos[0] + 18, dpos[1] + 6)), BLACK)
                draw.text(dpos, padNum(now.month), theme['secondary'], font=font)
                draw.text((dpos[0] + 7, dpos[1]), ".", theme['secondary'], font=font)
                draw.text((dpos[0] + 10, dpos[1]), padNum(now.day), theme['secondary'], font=font)
            else:
                if theme['border']:
                    draw.rectangle(((dpos[0] - 2, dpos[1] - 2), (dpos[0] + 13, dpos[1] + 6)), BLACK)
                draw.text(dpos, dayOfWeek, theme["secondary"], font=font)

def padNum(num):
    return "0" + str(num) if num < 10 else str(num)

if __name__ == '__main__':
    try:
        clock = Clock(50, 'hk2')
        clock.run()
    except KeyboardInterrupt:
        print('Interrupted with Ctrl-C')
        sys.exit(0)
