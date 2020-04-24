#!/usr/bin/python

from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
from datetime import datetime as dt
import time
import os

import sys  
sys.path.append('/home/pi/inky_fast')
from inky_fast import InkyFast

class InkyPHATFast(InkyFast):
    WIDTH = 212
    HEIGHT = 104

    WHITE = 0
    BLACK = 1
    RED = 2
    YELLOW = 2

    def __init__(self, colour):
        InkyFast.__init__(
            self,
            resolution=(self.WIDTH, self.HEIGHT),
            colour=colour,
            h_flip=False,
            v_flip=False)

inky_display = None
color = "black"

# Get the current path
PATH = os.path.dirname(__file__)

# Set the display type based on the time
inky_display = InkyPHAT(color)
# if dt.now().minute == 0 or dt.now().minute == 30:
#     # Slow update
#     inky_display = InkyPHAT(color)
# else:
#     # Fast update
#     inky_display = InkyPHATFast(color)

inky_display.set_border(inky_display.WHITE)

# Create the background
img = Image.open(os.path.join(PATH, "background.png"))
draw = ImageDraw.Draw(img)

# Write the time
timeFont = ImageFont.truetype(FredokaOne, 45)
hour = time.strftime("%H")
minutes = time.strftime("%M")

hourSizeX, hourSizeY = timeFont.getsize(hour)
minSizeX, minSizeY = timeFont.getsize(minutes)


hourX = (inky_display.WIDTH / 4) - 16 - (hourSizeX / 2)
minutesX = (inky_display.WIDTH / 4) - 16 - (minSizeX / 2)

hoursY = (inky_display.HEIGHT / 4)
minutesY = hoursY * 3

draw.text((timeX, (hoursY - (hourSizeY / 2))), hour, inky_display.BLACK, timeFont)
draw.text((timeX, (minutesY - (minSizeY / 2))), minutes, inky_display.BLACK, timeFont)

# Show on screen
inky_display.set_image(img)
inky_display.show()