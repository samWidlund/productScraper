import json
data = {
    "name": "sathiyajith",
    "rollno": 56,
    "cgpa": 8.6,
    "phone": "9976770500"
}

json_str = json.dumps(data, indent=4)
with open("my_file.json", "w") as f:
    f.write(json_str)