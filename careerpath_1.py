import json

def read_json(file_path):
    with open(file_path,'r') as file:
        return json.load(file)

careerpaths=read_json('career_path1.json')
studentdata=read_json('student_data1.json')

def calculate(career,studentdata):
    score=0
    max=0
    
    intmat=len(set(studentdata['interests']).intersection(career['interests']))
    score+=intmat*10
    max+=len(career['interests'])*10
    
    skillmat=0
    for skill,value in studentdata['skills'].items():
        if skill in career['skills']:
            if value>=8:
                skillmat+=1
            elif value>=5:
                skillmat+=0.5
    score+=skillmat*15
    max+=len(career['skills'])*15
    if career['economic']>studentdata['economical_status']:
        score+=(studentdata['economical_status']-career['economic'])*10
    else:
        score+= (studentdata['economical_status']-1)*10
    max+=15
    
    for sub,grad in studentdata['subjects'].items():
        if sub in career['subjects'] and grad in ['A','B']:
            score+=15
    max+=len(career['subjects'])*15
    
    for int in studentdata['peer_interests']:
        if int in career['interests']:
            score+=5
    max+=len(career['interests'])*5
    
    if studentdata['your_location'] == 'Urban':
        score+=10
        max+=10
    return (score/max)*100

def recommend(careerpaths,studentdata):
    rec=[]
    for car in careerpaths:
        score=calculate(car,studentdata)
        rec.append([car['career_name'],score])
    rec.sort(key=lambda x:x[1], reverse=True)
    return rec

rec_car=recommend(careerpaths,studentdata)
for rec,scor in rec_car:
    print(rec)
    
    
    
    
    