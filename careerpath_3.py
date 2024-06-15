import json
def read_json(file_path):
    with open(file_path,'r') as file:
        return json.load(file)

career_paths = read_json('career_path3.json')
student_data = read_json('student_data3.json')

def calculate(career,student):
    score=0
    max_score = 0
    int_match = len(set(career['interests']).intersection(set(student['interests'])))
    score +=int_match*10
    max_score +=len(career['interests'])*10
    
    skill_match=0
    for skill,value in student['skills'].items():
        if skill in career['skills']:
            if value>=8:
                skill_match+=1
            elif value >=5:
                skill_match+=0.5
    score+= skill_match*15
    max_score+=len(career['skills'])*15
    
    sub_match=0
    for sub,grad in student['subjects'].items():
        if sub in career['subjects'] and grad in ['A','B']:
            sub_match+=1
        elif sub in career['subjects'] and grad in ['C','D']:
            sub_match+=0.5
    score+=sub_match*5
    max_score+=len(career['subjects'])*5
    
    if career['Educational_Level'] == student['Educational_level']:
        score+=20
    max_score+=20
    return (score/max_score)*100

def recommend(career_paths,student_data):
    rec=[]
    
    for career in career_paths:
        score=calculate(career,student_data)
        if score>=30:
            rec.append([career,score])
    rec.sort(key=lambda x:x[1], reverse=True)
    return rec

for stud in student_data:
    rec_careers=recommend(career_paths,stud)
    choice=stud['Choice']
    if choice == 'Masters':
        print("Congratulations on embarking on your M.Tech journey! We wish you all the best as you pursue your goals and strive for excellence in your studies. Your determination and hard work will undoubtedly lead you to great success.")
        print("To support you further, we've compiled some valuable resources and information on important exams to help you along the way. These materials are designed to assist you in making informed decisions and to provide guidance as you prepare for your academic and professional future.")
        print("Should you need additional support or resources, please do not hesitate to visit us again. We are always here to help you achieve your aspirations.")
        print("Best of luck in all your endeavors!")
        
    elif choice == 'Startup':
        print("Congratulations on embarking on your entrepreneurial journey! We wish you all the best as you pursue your goals and strive for excellence in your business endeavors. Your innovation and hard work will undoubtedly lead you to great success.")
        print("To support you further, we've compiled some valuable resources and information on important aspects of starting and growing a business. These materials are designed to assist you in making informed decisions and to provide guidance as you navigate the entrepreneurial landscape.")
        print("Should you need additional support or resources, please do not hesitate to visit us again. We are always here to help you achieve your aspirations.")
        print("Best of luck in all your endeavors!")
    else:
        for career,score in rec_careers:
            if career['Educational_Level'] != stud['Educational_level']:
                print(f"{career['career_name']} - recommended higher education for better results :)")
            else: 
                print(career['career_name'])