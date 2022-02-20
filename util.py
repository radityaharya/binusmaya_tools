import csv
import datetime
import json
import os
import time
import pytz
import requests
from dateutil import parser
import re

institution = " "
roleId = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
Authorization = "Bearer xxxxxxxxxxxxxxxxxx"
rOId = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
academicCareer = " "


BASE_URL = "https://apim-bm7-prod.azure-api.net"
HEADERS = {    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "institution": institution,
    "roleId": roleId,
    "sec-ch-ua-mobile": "?0",
    "Authorization": Authorization,
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "academicCareer": academicCareer,
    "roleName": "Student",
    "sec-ch-ua-platform": "Windows",
    "Origin": "https://newbinusmaya.binus.ac.id",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://newbinusmaya.binus.ac.id/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,id;q=0.8",}
PAYLOAD = "{ }"


def getClassComponentList(period):
    url = (
        BASE_URL
        + f"/func-bm7-course-prod/Course/Period/{period}/ClassComponentList/Student"
    )
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    raise Exception(response.status_code)


# class component id = LAB,LEC,TUT
def getClassComponent(period, classComponentId):
    url = (
        BASE_URL
        + f"/func-bm7-course-prod/Course/Period/{period}/Component/{classComponentId}/Student"
    )
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    raise Exception(response.status_code)


def getClassSession(classId):
    url = BASE_URL + f"/func-bm7-course-prod/ClassSession/Class/{classId}/Student"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    raise Exception(response.status_code)


def getClassAttendance(classId):
    url = BASE_URL + f"/func-bm7-course-prod/SessionAttendance/Class/{classId}/Student"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    raise Exception(response.status_code)


def getSessionDetail(classSessionId):
    url = (
        BASE_URL
        + f"/func-bm7-course-prod/ClassSession/Session/{classSessionId}/Resource/Student?isWeb=true"
    )
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    raise Exception(response.status_code)


# forum


def getForum(classId):
    url = BASE_URL + f"/func-bm7-course-prod/Forum/Class/{classId}/Student"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    raise Exception(response.status_code)


def getForumTotalPost(classId, forumId):
    url = BASE_URL + f"/func-bm7-course-prod/Forum/Class/{classId}/Student/TotalPost"

    response = requests.post(url, headers=HEADERS, data=forumId)
    if response.status_code == 200:
        return response.json()
    raise Exception(response.status_code)


def getForumThread(classId, sessionId):
    url = f"https://apim-bm7-prod.azure-api.net/func-bm7-forum-prod/Thread/Class/{classId}/Session/{sessionId}/Paging/1"
    data = '{"TotalDataPerPage":10}'
    response = requests.post(url, headers=HEADERS, data=data)
    if response.status_code == 200:
        return response.json()
    raise Exception(response.status_code)


def getForumComment(threadId, forumId):
    url = BASE_URL + f"/func-bm7-forum-prod/Comment/Paging/1"
    payload = {
        "totalDataPerPage": 60,
        "parentId": threadId,
        "sortBy": "LatestPost",
        "forumId": forumId,
    }
    json_object = json.dumps(payload)
    response = requests.post(url, headers=HEADERS, data=json_object)
    if response.status_code == 200:
        return response.json()
    raise Exception(response.status_code)


def getScheduleMonth(date):
    if isinstance(date, str):
        date = parser.parse(date)
    date = date.strftime("%Y-%-m-" + "1")
    url = (
        f"https://func-bm7-schedule-prod.azurewebsites.net/api/Schedule/Month-v1/{date}"
    )
    res = json.loads(PAYLOAD)
    json_object = json.dumps(res, indent=4)
    response = requests.post(url, headers=HEADERS, data=json_object)

    if response.status_code == 200:
        return response.json()
    raise Exception(response.status_code)

def getScheduleDate(date):
    if isinstance(date, str):
        date = parser.parse(date)
    date = date.strftime("%Y-%-m-%-d")
    url = f"https://func-bm7-schedule-prod.azurewebsites.net/api/Schedule/Date-v1/{date}"

    res = json.loads(PAYLOAD)
    json_object = json.dumps(res, indent=4)
    response = requests.post(url, headers=HEADERS, data=json_object)
    if response.status_code == 200:
        return response.json()
    raise Exception(response.status_code)

#----- RESOURCE -----#


def getResource(resourceId):
    url = BASE_URL + f"/func-bm7-course-prod/ClassSession/Session/Resource/{resourceId}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response.status_code)

def getPptFromSessionId(sessionId):
    res = []
    resources = getSessionDetail(sessionId)["resources"]
    for i in range(len(resources)):
        if resources[i]["resourceType"] == "Document":
            res.append(resources[i])
    return res


def getNextClass():
    schedule = getScheduleDate(datetime.datetime.now())["Schedule"]
    for i in range(len(schedule)):
        if (
            datetime.datetime.strptime(schedule[i]["dateStart"], "%Y-%m-%dT%H:%M:%S")
            > datetime.datetime.now()
        ):
            return schedule[i]["customParam"]["classSessionId"]
    else:
        raise Exception("No next class")


def getNextClass2():
    schedule = getScheduleDate(datetime.datetime.now())["Schedule"]
    for i in range(len(schedule)):
        if datetime.datetime.strptime(
            schedule[i]["dateStart"], "%Y-%m-%dT%H:%M:%S"
        ) > datetime.datetime.now() and datetime.datetime.strptime(
            schedule[i]["dateStart"], "%Y-%m-%dT%H:%M:%S"
        ) < datetime.datetime.now() + datetime.timedelta(
            hours=2
        ):
            return schedule[i]["customParam"]["classSessionId"]


def getZoomLink(sessionId):
    sessionDetail = getSessionDetail(sessionId)["joinUrl"]
    return sessionDetail

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

        # convert 2022-02-21T08:50:00 to dd/mm/yyyy
        startDate = classSessionDetails[i]["dateStart"][0:10]
        startDate = startDate.split("-")
        startDate = startDate[2] + "/" + startDate[1] + "/" + startDate[0]

        # convert 2022-02-21T08:50:00 to hh:mm AM/PM using datetime strftime
        startTime = classSessionDetails[i]["dateStart"]
        startTime = startTime.split("T")
        startTime = startTime[1]
        startTime = startTime[0:5]
        startTime = time.strftime("%I:%M %p", time.strptime(startTime, "%H:%M"))

        endDate = classSessionDetails[i]["dateStart"][0:10]
        endDate = endDate.split("-")
        endDate = endDate[2] + "/" + endDate[1] + "/" + endDate[0]

        # convert 2022-02-21T08:50:00 to hh:mm AM/PM using datetime strftime
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

        item = {
            "Subject": f"[{classType}] {classSessionDetails[i]['course']}",
            "Start Date": startDate,
            "Start Time": startTime,
            "End Date": endDate,
            "End Time": endTime,
            "All Day Event": allDayEvent,
            "Description": Description,
            "Location": classSessionDetails[i]["classTitle"],
        }
        rows.append(item)

    tz  = pytz.timezone('Asia/Jakarta')
    now = datetime.datetime.now(tz)

    with open(f"gcal_{now}.csv", "w", encoding="UTF8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(rows)

def resourceDownloader(classTitle, courseName, session, topic, url):
    
    
    if url == "" or url == None:
        print(f"Invalid URL at {classTitle}\nsession {session}\ntopic {topic}" )
        return
    
    courseName = f"{classTitle}_{courseName}"
    if not os.path.exists("resources/" + courseName):
        os.makedirs("resources/" + courseName)
    r = requests.get(url, stream=True)

    filename = f"{session}_{topic}"
    #make filename filesystem safe
    filename = re.sub(r"[^A-Za-z0-9]+", " ", filename)
    
    if os.path.exists(f"resources/{courseName}/{filename}.pptx"):
        print(f"{filename} already exists")
        return

    time.sleep(2)
    with open(f"resources/{courseName}/{filename}.pptx", "wb") as pptx:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                pptx.write(chunk)