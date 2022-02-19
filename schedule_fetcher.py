import json
import time
import util
import os
import csv


PERIOD="2120"

classSessionDetails = []
classSessionDetailsRaw = []


def make_json(filename, dict):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        os.mknod(filename)
    with open(filename, "w") as f:
        f.truncate(0)
        json.dump(dict, f, indent=4)


class_actuall = []
for i in ["LEC", "LAB", "TUT"]:
    time.sleep(3)
    classes = util.getClassComponent(PERIOD, classComponentId=i)
    for a in range(len(classes)):
        courseName = classes[a]["courseName"]
        classId = classes[a]["classId"]
        classType = classes[a]["ssrComponent"]
        classCode = classes[a]["classCode"]
        class_actual = util.getClassSession(classId)
        class_actuall.append(class_actual)
        for b in range(100):
            try:
                classSessionId = class_actual["sessions"][b]["id"]
                # time.sleep(1)
                detail = util.getSessionDetail(classSessionId)
                topic = detail["topic"]
                print(topic)
                meetingStart = detail["meetingStart"]
                meetingEnd = detail["meetingEnd"]
                sessionNumber = detail["sessionNumber"]
                startDate = detail["dateStart"]
                dateEnd = detail["dateEnd"]
                deliveryMode = detail["deliveryMode"]
                joinUrl = detail["joinUrl"]
                courseSubTopic = []
                for subtopic in range(len(detail["courseSubTopic"])):
                    courseSubTopic.append(detail["courseSubTopic"][subtopic])
                classSessionDetailsRaw.append(detail)
                classSessionDetails.append(
                    {
                        "course": courseName,
                        "classTitle": f"{classCode} - {classType}",
                        "topic": topic,
                        "meetingStart": meetingStart,
                        "meetingEnd": meetingEnd,
                        "sessionNumber": sessionNumber,
                        "dateStart": startDate,
                        "dateEnd": dateEnd,
                        "deliveryMode": deliveryMode,
                        "courseSubtopic": courseSubTopic,
                        "joinUrl": joinUrl,
                        "classId": classId,
                        "classSessionId": classSessionId,
                    }
                )
            except:
                pass

make_json("classSessionDetails.json", classSessionDetails)
make_json("classSessionDetailsRaw.json", classSessionDetailsRaw)

print(classSessionDetails[0])

field_names = [
    "course",
    "classTitle",
    "topic",
    "meetingStart",
    "meetingEnd",
    "sessionNumber",
    "dateStart",
    "dateEnd",
    "deliveryMode",
    "courseSubtopic",
    "joinUrl",
    "classId",
    "classSessionId",
]


rows = []
for i in range(len(classSessionDetails)):
    rows.append(classSessionDetails[i])

if os.path.exists("classSessionDetails.csv"):
    os.remove("classSessionDetails.csv")
else:
    os.mknod("classSessionDetails.csv")

with open("classSessionDetails.csv", "w", encoding="UTF8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(rows)


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

    if classSessionDetails[i]["joinUrl"] in ("", None):
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

if os.path.exists("import_me_to_google_cal.csv"):
    os.remove("import_me_to_google_cal.csv")
else:
    os.mknod("import_me_to_google_cal.csv")

with open("import_me_to_google_cal.csv", "w", encoding="UTF8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(rows)
