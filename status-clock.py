#!/usr/bin/python

from inky import InkyPHAT as InkySlow
from inky_mod import InkyPHAT as InkyFast
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
from datetime import datetime as dt
import requests
import time
import textwrap
import os
import sys

# Inky displays defaults
inky_display = None
color = "black"

def clean_screen():
    if dt.now().minute == 0 and dt.now().hour == 10:
        start_cleaning()
    elif dt.now().minute == 15 and dt.now().hour == 10:
        start_cleaning()

def start_cleaning():
    inky_display = InkySlow(color)
    cycles = 3
    colours = (inky_display.YELLOW, inky_display.BLACK, inky_display.WHITE)
    colour_names = (color, "black", "white")
    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    for i in range(cycles):
        print("Cleaning cycle %i\n" % (i + 1))
        for j, c in enumerate(colours):
            print("- updating with %s" % colour_names[j])
            inky_display.set_border(c)
            for x in range(inky_display.WIDTH):
                for y in range(inky_display.HEIGHT):
                    img.putpixel((x, y), c)
            inky_display.set_image(img)
            inky_display.show()
            time.sleep(1)
        print("\n")
    sys.exit(0)

# Get the current path
PATH = os.path.dirname(__file__)

# Set the display type based on the time
if dt.now().minute == 0 or dt.now().minute == 30:
    # Slow update
    inky_display = InkySlow(color)
else:
    # Fast update
    inky_display = InkyFast(color)

# Check if display need to be cleaned
clean_screen()

# Start the clock
inky_display.set_border(inky_display.WHITE)

# Create the background
img = Image.open(os.path.join(PATH, "background.png"))
draw = ImageDraw.Draw(img)

# Get the meeting details
# meetingReq = requests.get('http://0.0.0.0:1337/get')
# meetingJson = meetingReq.json()

# Write the meeting
meetingFont = ImageFont.truetype(os.path.join(PATH, "font/BetterPixels.ttf"), 16)
# meetingTitle = meetingJson.get('title')
meetingTitle = "Hey ... is it time for a chat??"
titleXLoc = (inky_display.WIDTH / 2) - 15
titleYLoc = (inky_display.HEIGHT / 2) + 5
titleLines = textwrap.wrap(meetingTitle, width = 22)
for line in titleLines:
    width, height = meetingFont.getsize(line)
    draw.text((titleXLoc, titleYLoc), line, inky_display.WHITE, meetingFont)
    titleYLoc += height

# meetingTime = meetingJson.get('time')
meetingTime = "tomorrow at 12:00 PM"
timeWidth, timeHeight = meetingFont.getsize(meetingTime)
timeXLoc = 212 - 10 - timeWidth
timeYLoc = 88
draw.text((timeXLoc, timeYLoc), meetingTime, inky_display.WHITE, meetingFont)

# Write the time
timeFont = ImageFont.truetype(FredokaOne, 45)
hour = time.strftime("%H")
minutes = time.strftime("%M")

hourSizeX, hourSizeY = timeFont.getsize(hour, stroke_width=2)
minSizeX, minSizeY = timeFont.getsize(minutes)

hourX = (inky_display.WIDTH / 4) - 20 - (hourSizeX / 2)
minutesX = (inky_display.WIDTH / 4) - 20 - (minSizeX / 2)

hoursY = (inky_display.HEIGHT / 4)
minutesY = hoursY * 3

draw.text((hourX+1, (hoursY - (hourSizeY / 2) - 5)), hour, inky_display.BLACK, timeFont)
draw.text((hourX-1, (hoursY - (hourSizeY / 2) - 5)), hour, inky_display.BLACK, timeFont)
draw.text((hourX, (hoursY - (hourSizeY / 2) - 5) + 1), hour, inky_display.BLACK, timeFont)
draw.text((hourX, (hoursY - (hourSizeY / 2) - 5) - 1), hour, inky_display.BLACK, timeFont)
draw.text((hourX, (hoursY - (hourSizeY / 2) - 5)), hour, inky_display.YELLOW, timeFont)
draw.text((minutesX, (minutesY - (minSizeY / 2) - 3)), minutes, inky_display.BLACK, timeFont)

# Show on screen
inky_display.set_image(img.rotate(180))
inky_display.show()