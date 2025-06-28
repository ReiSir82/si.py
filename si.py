from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
from dateutil.relativedelta import relativedelta

API_KEY = ""
CALENDAR_ID = ""

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
        print(start, end, evName)
else:
    print("No events today")
