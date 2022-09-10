import csv
import datetime
import json
import os
import time
import pytz
import requests
import re


def make_json(filename, dict):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        os.mknod(filename)
    with open(filename, "w") as f:
        f.truncate(0)
        json.dump(dict, f, indent=4)


def toGcalCSV(classSessionDetails):
    field_names = [
        "Subject",
        "Start Date",
        "Start Time",
        "End Date",
        "End Time",
        "All Day Event",
        "Description",
        "Location",
        "Private",
    ]

    rows = []
    for i in range(len(classSessionDetails)):
        classType = classSessionDetails[i]["deliveryMode"]

        startDate = classSessionDetails[i]["dateStart"][0:10]
        startDate = startDate.split("-")
        startDate = startDate[2] + "/" + startDate[1] + "/" + startDate[0]

        startTime = classSessionDetails[i]["dateStart"]
        startTime = startTime.split("T")
        startTime = startTime[1]
        startTime = startTime[0:5]
        startTime = time.strftime("%I:%M %p", time.strptime(startTime, "%H:%M"))

        endDate = classSessionDetails[i]["dateStart"][0:10]
        endDate = endDate.split("-")
        endDate = endDate[2] + "/" + endDate[1] + "/" + endDate[0]

        endTime = classSessionDetails[i]["dateEnd"]
        endTime = endTime.split("T")
        endTime = endTime[1]
        endTime = endTime[0:5]
        endTime = time.strftime("%I:%M %p", time.strptime(endTime, "%H:%M"))

        allDayEvent = "False"

        if (
            classSessionDetails[i]["joinUrl"] == ""
            or classSessionDetails[i]["joinUrl"] == None
        ):
            url = (
                "https://newbinusmaya.binus.ac.id/lms/course/"
                + classSessionDetails[i]["classId"]
                + "/"
                + classSessionDetails[i]["classSessionId"]
            )
        else:
            url = classSessionDetails[i]["joinUrl"]

        Description = f"{url}\n\nSession: {classSessionDetails[i]['sessionNumber']}\n\n"
        for j in range(len(classSessionDetails[i]["courseSubtopic"])):
            Description += " - " + classSessionDetails[i]["courseSubtopic"][j] + "\n"
        
        if classSessionDetails[i]["location"] == None:
            location = "Virtual"
        else:
            location = classSessionDetails[i]["location"]
        
        item = {
            "Subject": f"[{classType}] {classSessionDetails[i]['course']}",
            "Start Date": startDate,
            "Start Time": startTime,
            "End Date": endDate,
            "End Time": endTime,
            "All Day Event": allDayEvent,
            "Description": Description,
            "Location": f'{classSessionDetails[i]["classTitle"]} - {location}',
        }
        rows.append(item)

    tz = pytz.timezone("Asia/Jakarta")
    now = datetime.datetime.now(tz)

    with open(f"gcal_{now}.csv", "w", encoding="UTF8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(rows)


def resourceDownloader(classTitle, courseName, session, topic, url):

    if url == "" or url == None:
        print(f"Invalid URL at {classTitle}\nsession {session}\ntopic {topic}")
        return

    courseName = f"{classTitle}_{courseName}"
    if not os.path.exists("resources/" + courseName):
        os.makedirs("resources/" + courseName)
    r = requests.get(url, stream=True)

    filename = f"{session}_{topic}"
    filename = re.sub(r"[^A-Za-z0-9]+", " ", filename)

    if os.path.exists(f"resources/{courseName}/{filename}.pptx"):
        print(f"{filename} already exists")
        return

    time.sleep(2)
    with open(f"resources/{courseName}/{filename}.pptx", "wb") as pptx:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                pptx.write(chunk)
