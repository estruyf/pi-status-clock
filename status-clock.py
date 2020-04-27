#!/usr/bin/python

from inky import InkyPHAT as InkySlow
from inky_mod import InkyPHAT as InkyFast
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
from datetime import datetime as dt
import requests
import time
import os

# meetingReq = requests.get('http://0.0.0.0:1337/get')
# meetingJson = meetingReq.json()

inky_display = None
color = "black"

# Get the current path
PATH = os.path.dirname(__file__)

# Set the display type based on the time
if dt.now().minute == 0 or dt.now().minute == 30:
    # Slow update
    inky_display = InkySlow(color)
else:
    # Fast update
    inky_display = InkyFast(color)

inky_display.set_border(inky_display.WHITE)

# Create the background
img = Image.open(os.path.join(PATH, "background.png"))
draw = ImageDraw.Draw(img)

# Write the meeting
meetingFont = ImageFont.truetype(FredokaOne, 16)
# meetingTitle = meetingJson.get('title')
meetingTitle = "Hey ... is it time for a chat??"
titleX, titleY = meetingFont.getsize(meetingTitle)
titleXLoc = (inky_display.WIDTH / 2)
titleYLoc = (inky_display.HEIGHT / 2) + 5
draw.text((titleXLoc, titleYLoc), meetingTitle, inky_display.WHITE, meetingFont)

# meetingTime = meetingJson.get('time')
# timeX, timeY = timeFont.getsize(minutes)

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

draw.text((hourX, (hoursY - (hourSizeY / 2) - 5)), hour, inky_display.BLACK, timeFont)
draw.text((minutesX, (minutesY - (minSizeY / 2) - 3)), minutes, inky_display.BLACK, timeFont)

# Show on screen
inky_display.set_image(img)
inky_display.show()