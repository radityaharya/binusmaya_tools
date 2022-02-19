import datetime
import json
import os
import requests
from dateutil import parser

BASE_URL = "https://apim-bm7-prod.azure-api.net"
HEADERS = {}

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