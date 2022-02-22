import json
from util import resourceDownloader, getResource


# load classSessionDetailsRaw.json
classSessionDetails = json.load(open("classSessionDetails.json"))

#itterate through classSessionDetailsRaw
for i in range(len(classSessionDetails)):
    for j in range(len(classSessionDetails[i]["resouceIds"])):
        if classSessionDetails[i]["resouceIds"][j]["resourceType"] == "Document":
            courseName = classSessionDetails[i]["course"]
            session = classSessionDetails[i]["sessionNumber"]
            topic = classSessionDetails[i]["topic"]
            url = getResource(classSessionDetails[i]["resouceIds"][j]["resourceId"])
            url = url['url']
            classTitle = classSessionDetails[i]["classTitle"]
            print(f"Downloading {courseName} {session} {topic}")
            resourceDownloader(classTitle,courseName,session,topic,url)
