import json
import os
import traceback
from dotenv import load_dotenv
import pymongo
import datetime
import util
import pytz

timezone = pytz.timezone('Asia/Jakarta')

load_dotenv()

client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB")]
col = db[os.getenv("MONGO_COLLECTION")]

with open("classSessionDetails.json", "r") as f:
    data = json.load(f)

mongo_ids = []
for i in range(len(data)):

    idd = f"course/{data[i]['classId']}/session/{data[i]['classSessionId']}"

    startDateTime = data[i]["dateStart"]
    startDateTime = datetime.datetime.strptime(
        startDateTime, "%Y-%m-%dT%H:%M:%S"
    )
    startDateTime = timezone.localize(startDateTime)

    endDateTime = data[i]["dateEnd"]
    endDateTime = datetime.datetime.strptime(endDateTime, "%Y-%m-%dT%H:%M:%S")
    endDateTime = timezone.localize(endDateTime)

    now = datetime.datetime.utcnow()

    now = timezone.localize(now)

    url = (
        "https://newbinusmaya.binus.ac.id/lms/course/"
        + data[i]["classId"]
        + "/session/"
        + data[i]["classSessionId"]
    )

    if data[i]["joinUrl"] != "":
        joinUrl = data[i]["joinUrl"]
    else:
        joinUrl = "https://bot.otid.site/invalid"

    item_dict = {
        "_id": idd,
        "course": data[i]["course"],
        "course_class": data[i]["classTitle"],
        "class_mode": data[i]["deliveryMode"],
        "session_num": "Session " + str(data[i]["sessionNumber"]),
        "start_datetime": startDateTime,
        "end_datetime": endDateTime,
        "session_url": url,
        "vicon_url": joinUrl,
        "topic": data[i]["topic"],
        "subtopic": data[i]["courseSubtopic"],
        "datetime_added": now,
        "isDone": (startDateTime < now),
    }

    try:
        col.delete_one({"_id": idd})
        print(f"deleted{idd}")
    except:
        traceback.print_exc()
        pass
    print(f"inserting {data[i]['topic']}")
    mongo_ids.append(col.insert_one(item_dict).inserted_id)

util.make_json("mongo_ids.json", mongo_ids)