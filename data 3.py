import json


with open('student_data1.json', 'r') as file:
    data = json.load(file)

formatted_data = {
    "personal_data": {
        "name": data["personal_data[name]"],
        "age": int(data["personal_data[age]"]),
        "gender": data["personal_data[gender]"]
    },
    "interests": list(set(data["interests[]"])),
    # "skills": data["skill[]"],
    "skills": {skill[7:-1]: int(level) for skill, level in data.items() if skill.startswith("skills[") and level},
    "your_location": data["your_location"],
    "economical_status": data["economical_status"],
    "subjects": {
        "literature": data["subjects[literature]"],
        "physics": data["subjects[physics]"],
        "chemistry": data["subjects[chemistry]"],
        "mathematics": data["subjects[mathematics]"],
        "languages": data["subjects[languages]"],
        "biology": data["subjects[biology]"],
        "sports": data["subjects[sports]"]
    },
    "peer_interests": list(set(data["interests[]"])),
    "mindset": {
        "decision_making_style": data["mindset[decision_making_style]"],
        "career_expectations": data["mindset[career_expectations]"]
    },
    "reqd": int(data["reqd"])
}


with open('student_data1.json', 'w') as outfile:
    json.dump(formatted_data, outfile, indent=4)
