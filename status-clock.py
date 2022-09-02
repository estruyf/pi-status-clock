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
import glob

# Inky displays defaults
inky_display = None
color = "black"
meetingChars = 20

# Dictionaries to store icons
icons = {}

# Set the display type based on the time
if dt.now().minute == 0 or dt.now().minute == 30:
    # Slow update
    inky_display = InkySlow(color)
else:
    # Fast update
    inky_display = InkyFast(color)

def clean_screen():
    if dt.now().minute == 0 and dt.now().hour == 8:
        start_cleaning()
    elif dt.now().minute == 0 and dt.now().hour == 19:
        start_cleaning()
    elif dt.now().minute == 30 and dt.now().hour == 12:
        start_cleaning()

def start_cleaning():
    cycles = 4
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

def reindex_image(source, mask=(inky_display.WHITE, inky_display.BLACK, inky_display.YELLOW)):
    w, h = source.size
    img = Image.new(mode='P', size=(w, h))
    remapped = []
    pxmap = { 0:1, 1:0, 2:2 }
    for px in source.getdata():
        try:
            remapped.append(pxmap[px])
        except:
            remapped.append(pxmap[0])
    img.putdata(remapped)
    return img

# Get the current path
PATH = os.path.dirname(__file__)

# Load our icon files and generate masks
for icon in glob.glob(os.path.join(PATH, "assets/icon-*.png")):
    icon_name = icon.split("icon-")[1].replace(".png", "")
    icon_image = Image.open(icon)
    icons[icon_name] = reindex_image(icon_image)

# Check if display need to be cleaned
clean_screen()

# Start the clock
inky_display.set_border(inky_display.WHITE)

# Create the background
img = Image.open(os.path.join(PATH, "background.png"))
draw = ImageDraw.Draw(img)

# Get the meeting details
req = requests.get('http://0.0.0.0:1337/get')
reqData = req.json()

# # Write the meeting title
# meetingJson = reqData.get('meeting')
# meetingFont = ImageFont.truetype(os.path.join(PATH, "font/BetterPixels.ttf"), 16)
# meetingTitle = meetingJson.get('title')
# titleXLoc = (inky_display.WIDTH / 2) - 15
# titleYLoc = (inky_display.HEIGHT / 2) + 5
# titleLines = textwrap.wrap(meetingTitle, width = meetingChars)
# i = 0
# for line in titleLines:
#     width, height = meetingFont.getsize(line)
#     if i <= 1:
#         draw.text(((titleXLoc - (i * 5)), titleYLoc), line, inky_display.WHITE, meetingFont)
#         titleYLoc += height
#     i += 1

# # Write the meeting time
# meetingTime = meetingJson.get('time')
# timeWidth, timeHeight = meetingFont.getsize(meetingTime)
# timeXLoc = 212 - 5 - timeWidth
# timeYLoc = 88
# draw.text((timeXLoc, timeYLoc), meetingTime, inky_display.WHITE, meetingFont)

# Get the battery status
batteryPercentage = reqData.get('battery')
if batteryPercentage is not None:
    batteryFont = ImageFont.truetype(os.path.join(PATH, "font/BetterPixels.ttf"), 16)
    batteryText = str(batteryPercentage)
    batteryTextWidth, batteryTextHeight = batteryFont.getsize(batteryText)
    batteryX = inky_display.WIDTH - batteryTextWidth - 5
    batteryY = 52 + 30
    draw.text((batteryX, batteryY), batteryText, inky_display.WHITE, batteryFont)

# Write the temperature
temperature = reqData.get('temperature')
if temperature != None and temperature > 0:
    temperature = round(temperature) 

    degFont = ImageFont.truetype(os.path.join(PATH, "font/BetterPixels.ttf"), 16)
    tempFont = ImageFont.truetype(os.path.join(PATH, "font/BetterPixels.ttf"), 35)
    tempX = (inky_display.WIDTH / 2) + 5
    tempY = 15
    tempTxt = str(temperature)
    tempWidth, tempHeight = tempFont.getsize(tempTxt)
    draw.text((tempX, tempY), tempTxt, inky_display.WHITE, tempFont)

    # Degree symbol not supported with the font, we add an "o" instead
    draw.text((tempX + tempWidth, tempY), "o", inky_display.WHITE, degFont)

# Write the number of tasks
# todoTasks = reqData.get('todoTasks')
# if todoTasks is not None:
#     todoFont = ImageFont.truetype(os.path.join(PATH, "font/BetterPixels.ttf"), 35)
#     todoTxt = str(todoTasks)
#     todoWidth, todoHeight = todoFont.getsize(todoTxt)
#     todoX = inky_display.WIDTH - todoWidth - 5
#     todoY = 15
#     draw.text((todoX, todoY), todoTxt, inky_display.BLACK, todoFont)
#     img.paste(icons["todo"], ((inky_display.WIDTH - 15) - 5 - todoWidth, 35 - 9))

# Get the stars for Front Matter
stars = reqData.get('stars')
if stars is not None:
    starsFont = ImageFont.truetype(os.path.join(PATH, "font/BetterPixels.ttf"), 35)
    starsText = str(stars)
    todoWidth, todoHeight = starsFont.getsize(starsText)
    starsX = inky_display.WIDTH - todoWidth - 5
    starsY = 15
    draw.text((starsX, starsY), starsText, inky_display.BLACK, starsFont)
    # img.paste(icons["todo"], ((inky_display.WIDTH - 15) - 5 - todoWidth, 35 - 9))

# Write the availability
availability = reqData.get('availability')
if availability is not None:
    img.paste(icons[availability], (int((inky_display.WIDTH/2)-36), 17))

# Write the time
timeFont = ImageFont.truetype(FredokaOne, 45)

# Calculate and print hour
hour = time.strftime("%H")
hourSizeX, hourSizeY = timeFont.getsize(hour)
hourX = (inky_display.WIDTH / 4) - 20 - ((hourSizeX + 4) / 2) # spacing both ends
hoursY = (inky_display.HEIGHT / 4)
for char in hour:
    width, height = timeFont.getsize(char)
    draw.text((hourX+2, (hoursY - (height / 2) - 5)), char, inky_display.BLACK, timeFont)
    draw.text((hourX-2, (hoursY - (height / 2) - 5)), char, inky_display.BLACK, timeFont)
    draw.text((hourX, (hoursY - (height / 2) - 5) + 2), char, inky_display.BLACK, timeFont)
    draw.text((hourX, (hoursY - (height / 2) - 5) - 2), char, inky_display.BLACK, timeFont)
    draw.text((hourX, (hoursY - (height / 2) - 5)), char, inky_display.WHITE, timeFont)
    hourX += (width + 3)

# Print the minutes
minutes = time.strftime("%M")
minSizeX, minSizeY = timeFont.getsize(minutes)
minutesX = (inky_display.WIDTH / 4) - 20 - (minSizeX / 2)
minutesY = hoursY * 3
draw.text((minutesX, (minutesY - (minSizeY / 2) - 3)), minutes, inky_display.BLACK, timeFont)

# Show on screen
# inky_display.set_image(img.rotate(180))
inky_display.set_image(img)
inky_display.show()
