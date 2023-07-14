from PIL import Image, ImageDraw, ImageFont
import time
from datetime import datetime

light_pink = (255,219,218)
dark_pink = (219,127,142)
white = (230,255,255)

salmon = (255,150,162)
tan = (255,205,178)
orange_tinted_white = (248,237,235)

washed_out_navy = (109,104,117)

discordColor = (150,170,255)
messengerColor = (60, 220, 255)
snapchatColor = (255, 252, 0)
smsColor = (110, 255, 140)

spotify_color = (0,255,0)

class MainScreen:
    def __init__(self, config):
        self.font = ImageFont.truetype("fonts/tiny.otf", 5)

        self.canvas_width = config.getint('System', 'canvas_width', fallback=64)
        self.canvas_height = config.getint('System', 'canvas_height', fallback=32)
        self.cycle_time = config.getint('Main Screen', 'cycle_time', fallback=20)
        self.use_24_hour = config.getboolean('Main Screen', 'use_24_hour', fallback=False)

        self.lastGenerateCall = None
        self.on_cycle = True

        self.bgs = {'sakura' : Image.open('res/sakura-bg.png').convert("RGBA")}
        self.theme_list = [self.generateSakura]

        self.currentIdx = 0
        self.selectMode = False

        self.old_noti_list = []
        self.queued_frames = []

    def generate(self):

        if (self.lastGenerateCall is None):
            self.lastGenerateCall = time.time()
        if (time.time() - self.lastGenerateCall >= self.cycle_time):
            self.on_cycle = not self.on_cycle
            self.lastGenerateCall = time.time()

        frame = self.theme_list[0]()

        if (self.selectMode):
            draw = ImageDraw.Draw(frame)
            draw.rectangle((0,0,self.canvas_width-1,self.canvas_height-1), outline=white)

        return frame

    def generateSakura(self):
        currentTime = datetime.now()
        month = currentTime.month
        day = currentTime.day
        dayOfWeek = currentTime.weekday() + 1
        hours = currentTime.hour
        if not self.use_24_hour:
            hours = hours % 12
            if (hours == 0):
                hours += 12
        minutes = currentTime.minute

        frame = self.bgs['sakura'].copy()
        draw = ImageDraw.Draw(frame)

        draw.text((3, 6), padToTwoDigit(hours), light_pink, font=self.font)
        draw.text((10, 6), ":", light_pink, font=self.font)
        draw.text((13, 6), padToTwoDigit(minutes), light_pink, font=self.font)

        if (self.on_cycle):
            #date
            draw.text((23, 6), padToTwoDigit(month), dark_pink, font=self.font)
            draw.text((30, 6), ".", dark_pink, font=self.font)
            draw.text((33, 6), padToTwoDigit(day), dark_pink, font=self.font)
        else:
            #dayOfWeek
            draw.text((23, 6), padToTwoDigit(dayOfWeek), dark_pink, font=self.font)

        return frame

def padToTwoDigit(num):
    if num < 10:
        return "0" + str(num)
    else:
        return str(num)
