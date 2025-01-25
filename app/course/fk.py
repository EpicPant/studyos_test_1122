import json

with open("app/course/testing_data.json", "r") as file:
    data = json.load(file)

topics = list(data["course"]["topics"].keys())
for i in topics:
    topic_items = data["course"]["topics"][i].keys()
    