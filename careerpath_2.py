import json

def read_json(file_path):
    with open(file_path,'r') as file:
        return json.load(file)
    
career_p=read_json('career_path2.json')
student=read_json('student_data2.json')

def calculate(career,student):
    score=0
    max=0
    
    intmat=len(set(student['interests']).intersection(career['interests']))
    score+=intmat*10
    max+=len(career['interests'])
    
    for skill,value in student['skills'].items():
        if skill in career['skills']:
            if value>=8:
                score+=15
            elif value>=5:
                score+=7.5
    max+=len(career['skills'])*15
    
    score+=(student['economical_status']-1)*15
    max+=45
    
    for sub,grad in student['subjects'].items():
        if sub in career['subjects'] and grad in ['A','B']:
            score+=10
        elif sub in career['subjects'] and grad in ['C','D']:
            score+=5
    max+=len(career['subjects'])*15
    
    for int in student['peer_interests']:
        if int in career['interests']:
            score+=5
    max+=len(career['interests'])*5
    
    if student['your_location'] == 'Urban':
        score+=10
        max+=10
    return (score/max)*100

def recommend(careerpaths,studentdata):
    rec=[]
    for car in careerpaths:
        score=calculate(car,studentdata)
        if score>=30:
            rec.append([car['career_name'],score])
    rec.sort(key=lambda x:x[1], reverse=True)
    return rec

rec_car=recommend(career_p,student)
for rec,scor in rec_car:
    print(rec)
    