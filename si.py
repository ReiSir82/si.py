import time, sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
from dateutil.relativedelta import relativedelta

API_KEY = "AIzaSyBVHAvSefPy5KA9-NMvz17GPbPGnjB6Hbc"

CALENDAR_ID = "cbed25114523a40fd7f70f7af6b8e46a3fd0c585ee607f221b5279782047af8d@group.calendar.google.com"

def getEvents(calId, apiKey, startTime, endTime):
    try:
        service = build("calendar", "v3", developerKey=apiKey)
        response = service.events().list(
            calendarId=calId,
            timeMin=startTime.isoformat() + "Z",
            timeMax=endTime.isoformat() + "Z",
            singleEvents=True,
            orderBy="startTime").execute()
        return response.get("items", [])
    except HttpError as error:
        print(error)

now = datetime.datetime.now()
today0am   = now + relativedelta(hour=0, minute=0)
tomorow0am = now + relativedelta(days=+1, hour=0, minute=0)

events = getEvents(CALENDAR_ID, API_KEY, today0am, tomorow0am)
#     print(events)

if len(events) != 0:
    for event in events:
        start = event["start"]["dateTime"]
    end   = event["end"]["dateTime"]
    evName = event["summary"]
    startDate = start.split("T")[0]
    print(startDate)
    mo = startDate.split("-")[1]
    day = startDate.split("-")[2]
    print(mo, day)
    a = start.split("T")[1]
    hr = a.split(":")[0]
    min = a.split(":")[1]
    print(hr, min)
    
    
    
    
else:
    print("No events today")
    
    

options = RGBMatrixOptions()
options.cols = 64
options.rows = 64
options.parallel = 1
options.gpio_slowdown = 3
options.drop_privileges=False

panelImageFileName = "panel.jpg"
imageWidth = 64
imageHeight = 64

image = Image.new("RGB", (imageWidth, imageHeight), (0, 0, 0))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

draw.text((0, 0), startDate, fill=(255, 0, 0), font=font)
draw.text((0, 8), hr, fill=(0, 0, 255), font=font)
draw.text((18, 8), min, fill=(0, 0, 255), font=font)
draw.text((0, 16), evName, fill=(255, 255, 255), font=font)
draw.text((0, 30), "2025-06-27", fill=(255, 0, 0), font=font)
draw.text((0, 38), "15 30", fill=(0, 0, 255), font=font)
draw.text((0, 46), "Event 2", fill=(255, 255, 255), font=font)

image.save(panelImageFileName)

matrix = RGBMatrix(options = options)
matrix.SetImage(image)

while True:
    try:
        time.sleep(100)
    except KeyboardInterrupt:
        break

