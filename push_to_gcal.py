import json
import datetime
from datetime import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from util import make_json

CAL_ID = "xxxxxxxx@group.calendar.google.com"
#or "primary" pr "your_gmail@gmail.com"


SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_FILE = ".credentials/credentials.json"
creds = None

if os.path.exists("token.pickle"):
    with open("token.pickle", "rb") as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
    with open("token.pickle", "wb") as token:
        pickle.dump(creds, token)

service = build("calendar", "v3", credentials=creds)

with open("classSessionDetails.json") as f:
    data = json.load(f)

try:
    with open("cal_ids.json") as f:
        event_ids = json.load(f)

    print("deleting events")
    for event_id in event_ids:
        print("deleting event: " + event_id)
        service.events().delete(calendarId=CAL_ID, eventId=event_id).execute()
except:
    print("no cal_ids.json")


ids = []
for i in range(len(data)):

    startDateTime = data[i]["dateStart"]
    startDateTime = datetime.strptime(startDateTime, "%Y-%m-%dT%H:%M:%S").strftime(
        "%Y-%m-%dT%H:%M:%S"
    )

    endDateTime = data[i]["dateEnd"]
    endDateTime = datetime.strptime(endDateTime, "%Y-%m-%dT%H:%M:%S").strftime(
        "%Y-%m-%dT%H:%M:%S"
    )

    if data[i]["joinUrl"] == "" or data[i]["joinUrl"] == None:
        url = (
            "https://newbinusmaya.binus.ac.id/lms/course/"
            + data[i]["classId"]
            + "/session/"
            + data[i]["classSessionId"]
        )
    else:
        url = data[i]["joinUrl"]

    Description = f"{url}\n\nSession: {data[i]['sessionNumber']}\n\n"
    for j in range(len(data[i]["courseSubtopic"])):
        Description += " - " + data[i]["courseSubtopic"][j] + "\n"
    classType = data[i]["deliveryMode"]

    #colorrrrrr
    #id     name        hex
    # 1	    Lavender	#7986cb
    # 2	    Sage	    #33b679
    # 3	    Grape	    #8e24aa
    # 4	    Flamingo	#e67c73
    # 5	    Banana	    #f6c026
    # 6	    Tangerine	#f5511d
    # 7	    Peacock 	#039be5
    # 8	    Graphite	#616161
    # 9	    Blueberry	#3f51b5
    # 10	Basil       #0b8043
    # 11	Tomato  	#d60000

    color = ""
    if data[i]["course"][0:7] == "Advance":
        color = "5"
    else:
        color = "2"

    start = {"dateTime": str(startDateTime), "timeZone": "Asia/Jakarta"}
    end = {"dateTime": str(endDateTime), "timeZone": "Asia/Jakarta"}
    summary = f"[{classType}] {data[i]['course']}"
    location = data[i]["classTitle"]
    description = Description
    colorId = color

    event = {
        "summary": summary,
        "location": location,
        "description": description,
        "colorId": colorId,
        "start": start,
        "end": end,
    }

    event = service.events().insert(calendarId=CAL_ID, body=event).execute()

    ids.append(event["id"])


make_json("cal_ids.json", ids)
