from PIL import Image, ImageDraw, ImageFont
import time
from datetime import datetime

light_pink = (255,219,218)
dark_pink = (219,127,142)
white = (230,255,255)

salmon = (255,150,162)
tan = (255,205,178)
orange_tinted_white = (248,237,235)

black = (0, 0, 0)
dark_red = (46, 0, 51)

cyan = (128, 247, 255)

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
                'date': True,
                'datepos': (23, 6),
                'primary': light_pink,
                'secondary': dark_pink,
                'border': False,
            },
            'cat' : {
                'image': 'res/cat.jpg',
                'timepos': (3, 6),
                'date': True,
                'datepos': (23, 6),
                'primary': light_pink,
                'secondary': dark_pink,
                'border': False,
            },
            'dm' : {
                'image': 'res/dm.jpg',
                'timepos': (45, 2),
                'date': True,
                'datepos': (45, 8),
                'primary': light_pink,
                'secondary': dark_pink,
                'border': False,
            },
            'flowers' : {
                'image': 'res/flowers.jpg',
                'timepos': (3, 6),
                'date': True,
                'datepos': (23, 6),
                'primary': light_pink,
                'secondary': dark_pink,
                'border': False,
            },
            'ponyo' : {
                'image': 'res/ponyo.jpg',
                'timepos': (4, 4),
                'date': False,
                'datepos': (4, 4),
                'primary': white,
                'secondary': cyan,
                'border': True,
            },
            'hk1' : {
                'image': 'res/hk1.png',
                'timepos': (3, 6),
                'date': True,
                'datepos': (23, 6),
                'primary': light_pink,
                'secondary': dark_pink,
                'border': False,
            },
            'hk2' : {
                'image': 'res/hk2.png',
                'timepos': (3, 6),
                'date': True,
                'datepos': (23, 6),
                'primary': light_pink,
                'secondary': dark_pink,
                'border': False,
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

def padNum(num):
    return "0" + str(num) if num < 10 else str(num)

def set_datetime(frame, theme, show_day):
    currentTime = datetime.now()
    month = currentTime.month
    day = currentTime.day
    dayOfWeek = currentTime.strftime("%A")[:3].upper()
    hours = currentTime.hour
    minutes = currentTime.minute

    font = ImageFont.truetype("fonts/tiny.otf", 5)
    draw = ImageDraw.Draw(frame)

    tpos = theme['timepos']
    dpos = theme['datepos']

    if (theme['border']):
        draw.rectangle(((tpos[0] - 2, tpos[1] - 2), (tpos[0] + 18, tpos[1] + 6)), black)

    draw.text(tpos, padNum(hours), theme['primary'], font=font)
    draw.text((tpos[0] + 7, tpos[1]), ":", theme['primary'], font=font)
    draw.text((tpos[0] + 10, tpos[1]), padNum(minutes), theme['primary'], font=font)

    if theme['date']:
        if show_day:
            if theme['border']:
                draw.rectangle(((dpos[0] - 2, dpos[1] - 2), (dpos[0] + 18, dpos[1] + 6)), black)
            draw.text(dpos, padNum(month), theme['secondary'], font=font)
            draw.text((dpos[0] + 7, dpos[1]), ".", theme['secondary'], font=font)
            draw.text((dpos[0] + 10, dpos[1]), padNum(day), theme['secondary'], font=font)
        else:
            if theme['border']:
                draw.rectangle(((dpos[0] - 2, dpos[1] - 2), (dpos[0] + 13, dpos[1] + 6)), black)
            draw.text(dpos, dayOfWeek, theme["secondary"], font=font)
