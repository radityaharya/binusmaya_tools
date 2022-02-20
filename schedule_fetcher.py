import time
import util


PERIOD="2120"

classSessionDetails = []
classSessionDetailsRaw = []

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
                resIds = detail["resources"]
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
                        "resourceId": resIds
                    }
                )
            except:
                pass

util.make_json("classSessionDetails.json", classSessionDetails)
util.make_json("classSessionDetailsRaw.json", classSessionDetailsRaw)

util.toGcalCSV(classSessionDetails)