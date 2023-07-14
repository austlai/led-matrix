from PIL import Image, ImageDraw, ImageFont
import time
from datetime import datetime

light_pink = (255,219,218)
dark_pink = (219,127,142)
white = (230,255,255)

salmon = (255,150,162)
tan = (255,205,178)
orange_tinted_white = (248,237,235)

red = (150, 1, 8)
dark_red = (102, 0, 51)

washed_out_navy = (109,104,117)

discordColor = (150,170,255)
messengerColor = (60, 220, 255)
snapchatColor = (255, 252, 0)
smsColor = (110, 255, 140)

spotify_color = (0,255,0)

class Default:
    def __init__(self, config):
        self.canvas_width = config.getint('System', 'canvas_width', fallback=64)
        self.canvas_height = config.getint('System', 'canvas_height', fallback=32)

        self.loop_time = 20
        self.show_day = True
        self.updateTime= None

        self.themes = {
            'sakura' : {
                'image': 'res/sakura.png',
                'timepos': (3, 6),
                'datepos': (23, 6),
                'primary_colour': light_pink,
                'secondary_colour': dark_pink,
            },
            'cat' : {
                'image': 'res/cat.jpg',
                'timepos': (3, 6),
                'datepos': (23, 6),
                'primary_colour': light_pink,
                'secondary_colour': dark_pink,
            },
            'dm' : {
                'image': 'res/dm.jpg',
                'timepos': (3, 6),
                'datepos': (23, 6),
                'primary_colour': light_pink,
                'secondary_colour': dark_pink,
            },
            'flowers' : {
                'image': 'res/flowers.jpg',
                'timepos': (3, 6),
                'datepos': (23, 6),
                'primary_colour': light_pink,
                'secondary_colour': dark_pink,
            },
            'ponyo' : {
                'image': 'res/ponyo.jpg',
                'timepos': (5, 6),
                'datepos': (3, 12),
                'primary_colour': dark_red,
                'secondary_colour': red,
            },
        }

    def generate(self):
        if (self.updateTime is None):
            self.updateTime= time.time()
        if (time.time() - self.updateTime>= self.loop_time):
            self.show_day = not self.show_day
            self.updateTime = time.time()

        theme = self.themes['ponyo']
        frame = Image.open(theme['image']).convert("RGB")

        set_datetime(frame, theme, self.show_day)

        return frame

def padToTwoDigit(num):
    return "0" + str(num) if num < 10 else str(num)

def set_datetime(frame, theme, show_day):
    currentTime = datetime.now()
    month = currentTime.month
    day = currentTime.day
    dayOfWeek = currentTime.strftime("%A")[:3]
    hours = currentTime.hour
    minutes = currentTime.minute

    font = ImageFont.truetype("fonts/tiny.otf", 5)
    draw = ImageDraw.Draw(frame)

    tpos = theme['timepos']
    dpos = theme['datepos']

    draw.text(tpos, padToTwoDigit(hours), theme['primary_colour'], font=font)
    draw.text((tpos[0] + 7, tpos[1]), ":", theme['primary_colour'], font=font)
    draw.text((tpos[0] + 10, tpos[1]), padToTwoDigit(minutes), theme['primary_colour'], font=font)

    if (show_day):
        draw.text(dpos, padToTwoDigit(month), theme['secondary_colour'], font=font)
        draw.text((dpos[0] + 7, dpos[1]), ".", theme['secondary_colour'], font=font)
        draw.text((dpos[0] + 10, dpos[1]), padToTwoDigit(day), theme['secondary_colour'], font=font)
    else:
        draw.text(dpos, dayOfWeek, dark_pink, font=font)
