import datetime
import os
import time
from tqdm import tqdm
import util
from binusmaya import bimay
from dotenv import load_dotenv

load_dotenv()


def fetch_schedule():
    classSessionDetails = []
    bm = bimay.bimay(token=os.getenv("TOKEN"), roleId=os.getenv("ROLEID"))
    academicPeriod = bm.get_latest_academicPeriod()
    termBeginDate = datetime.datetime.strptime(
        academicPeriod["termBeginDate"], "%Y-%m-%dT%H:%M:%S"
    )
    termEndDate = datetime.datetime.strptime(
        academicPeriod["termEndDate"], "%Y-%m-%dT%H:%M:%S"
    )
    print("start date: " + str(termBeginDate))
    print("end date: " + str(termEndDate))

    print("this may take a while...")
    schedules = bm.get_schedule_month(termBeginDate, termEndDate)
    print(len(schedules["Schedule"]))
    for i in tqdm(range(len(schedules["Schedule"]))):
        time.sleep(0.5)
        classSessionId = schedules["Schedule"][i]["customParam"]["classSessionId"]
        detail = bm.get_class_session_detail(classSessionId)
        if detail == None:
            continue
        courseSubTopic = []
        for subtopic in range(len(detail["courseSubTopic"])):
            courseSubTopic.append(detail["courseSubTopic"][subtopic])
        classSessionDetails.append(
            {
                "course": schedules["Schedule"][i]["content"],
                "classTitle": schedules["Schedule"][i]["title"],
                "topic": detail["topic"],
                "meetingStart": detail["meetingStart"],
                "meetingEnd": detail["meetingEnd"],
                "sessionNumber": detail["sessionNumber"],
                "dateStart": detail["dateStart"],
                "dateEnd": detail["dateEnd"],
                "deliveryMode": detail["deliveryMode"],
                "courseSubtopic": courseSubTopic,
                "joinUrl": detail["joinUrl"],
                "classId": schedules["Schedule"][i]["customParam"]["classId"],
                "classSessionId": classSessionId,
                "resourceId": detail["resources"],
                "deliveryMode": schedules["Schedule"][i]["deliveryMode"],
                "location": schedules["Schedule"][i]["location"],
                "scheduleType": schedules["Schedule"][i]["scheduleType"],
            }
        )
    return classSessionDetails


if __name__ == "__main__":
    classSessionDetails = fetch_schedule()
    util.make_json("classSessionDetails.json", classSessionDetails)

    util.toGcalCSV(classSessionDetails)
