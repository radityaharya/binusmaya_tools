import datetime
from datetime import datetime
import json
import time
from notion_client import Client
from dotenv import load_dotenv
import util
from tqdm import tqdm
import os

load_dotenv()
notion = Client(auth=os.getenv("NOTION_TOKEN"))

NOTION_DATABASE_NAME = os.getenv("NOTION_DATABASE_NAME")

search_database = notion.search(**{"query": NOTION_DATABASE_NAME, "value": "database"})


my_database_id = search_database["results"][0]["id"]
my_database = notion.databases.retrieve(database_id=my_database_id)

results = notion.databases.query(
    **{
        "database_id": my_database_id,
    }
).get("results")


for block in results:
    block_id = block["id"]
    print("deleting ", block_id)
    notion.blocks.delete(block_id)


with open("classSessionDetails.json") as f:
    data = json.load(f)

for i in tqdm(range(len(data))):
    startDateTime = data[i]["dateStart"]
    startDateTime = datetime.strptime(startDateTime, "%Y-%m-%dT%H:%M:%S").strftime(
        "%Y-%m-%dT%H:%M:%S.%f+07:00"
    )

    endDateTime = data[i]["dateEnd"]
    endDateTime = datetime.strptime(endDateTime, "%Y-%m-%dT%H:%M:%S").strftime(
        "%Y-%m-%dT%H:%M:%S.%f+07:00"
    )

    course = data[i]["course"]
    topic = data[i]["topic"]
    classTitle = data[i]["classTitle"]
    deliveryMode = data[i]["deliveryMode"]
    sessionNumber = data[i]["sessionNumber"]
    pptLink = None
    resources = data[i]["resouceIds"]
    for i in range(len(resources)):
        if resources[i]["resourceType"] == "Document":
            pptLink = resources[i]["url"]
    subtopic = ""
    for j in range(len(data[i]["courseSubtopic"])):
        subtopic += " - " + data[i]["courseSubtopic"][j] + "\n"
    joinUrl = None
    if data[i]["joinUrl"] != "":
        joinUrl = data[i]["joinUrl"]
    url = (
        "https://newbinusmaya.binus.ac.id/lms/course/"
        + data[i]["classId"]
        + "/session/"
        + data[i]["classSessionId"]
    )

    new_page_props = {
        "Zoom Link": {"type": "url", "url": joinUrl},
        "URL": {"type": "url", "url": url},
        "Delivery Mode": {
            "type": "select",
            "select": {
                "name": deliveryMode,
            },
        },
        "Subtopic": {
            "type": "rich_text",
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": subtopic,
                    },
                    "plain_text": subtopic,
                }
            ],
        },
        "End": {
            "type": "date",
            "date": {
                "start": str(startDateTime),
            },
        },
        "Start": {
            "type": "date",
            "date": {
                "start": str(endDateTime),
            },
        },
        "Course": {
            "type": "select",
            "select": {
                "name": course,
            },
        },
        "PPT": {"type": "url", "url": util.urlshorter(pptLink)},
        "Session": {"type": "number", "number": int(sessionNumber)},
        "Class": {
            "type": "select",
            "select": {
                "name": classTitle,
            },
        },
        "Topic": {
            "type": "title",
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": topic,
                    },
                    "plain_text": topic,
                }
            ],
        },
    }

    notion_page = notion.pages.create(
        parent={"database_id": my_database["id"]}, properties=new_page_props
    )
    if notion_page["object"] == "error":
        print("ERROR", notion_page["message"])
        continue
