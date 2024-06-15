import json

def read_json(file_path):
    with open(file_path,'r') as file:
        return json.load(file)

jobs_data= read_json('jobs.json')
input_datas = read_json('input.json')
for input_data in input_datas:
    input_job= input_data['job_name']
    input_skills = list(input_data['skills'])
    input_values = list(input_data['values'])
    for job in jobs_data:
        if job['job_name'] == input_job:
            skills = job['skills']
            print(job['job_name'],end=":\n")
            flag=True
            for skill in skills:
                if skill in input_skills:
                    if input_values[input_skills.index(skill)] < 8:
                        print(f"{skill} - improve")
                else:
                    print(f"{skill} - needed")
                    flag=False
            if flag:
                print("You have all the required skills at required level") 
            break
    print("")
