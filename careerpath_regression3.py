import json
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def prepare_data(career_paths, student_data):
        X = []
        y = []

        student_interests = set(student_data['interests'])
        student_skills = student_data['skills']
        student_subjects = student_data['subjects']
        
        for career in career_paths:
            career_interests = set(career['interests'])
            career_skills = career['skills']
            career_subjects = career['subjects']
            
            int_match = len(student_interests.intersection(career_interests)) * 10
            for int in student_data['peer_interests']:
                if int in career['interests']:
                    int_match+=5
            skill_match=0
            for skill in career_skills:
                if student_skills.get(skill,0) >=8:
                    skill_match+=1
                elif student_skills.get(skill,0) >=5:
                    skill_match+=0.5
            skill_match*=15
            sub_match=0
            for sub in career_subjects:
                if student_subjects.get(sub,'') in ['A','B']:
                    sub_match+=1
                elif student_subjects.get(sub,'') in ['C','D']:
                    sub_match+=0.5
            sub_match*=15
            education_match = 20 if student_data['Educational_level'] == career['education_level'] else 0
            salarybias=career['Expected_Salary']/600000 *20
            
            score = (int_match + skill_match + sub_match + education_match + salarybias) /(len(career_interests)*15+len(career_skills)*15+len(career_subjects)*15) * 100
            
            X.append([int_match, skill_match, sub_match, education_match,salarybias])
            y.append(score)
    
        return X,y

def train_regression_model(X, y):
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_val)
    mse = mean_squared_error(y_val, y_pred)
    
    return model

def recommend_careers(model, career_paths, student):
    X_pred = []
    student_interests = set(student['interests'])
    student_skills = student['skills']
    student_subjects = student['subjects']
    
    for career in career_paths:
        career_interests = set(career['interests'])
        career_skills = career['skills']
        career_subjects = career['subjects']
        
        int_match = len(student_interests.intersection(career_interests)) * 10
        for int in student['peer_interests']:
            if int in career['interests']:
                int_match+=5
        skill_match=0
        for skill in career_skills:
            if student_skills.get(skill,0) >=8:
                skill_match+=1
            elif student_skills.get(skill,0) >=5:
                skill_match+=0.5
        skill_match*=15
        sub_match=0
        for sub in career_subjects:
            if student_subjects.get(sub,'') in ['A','B']:
                sub_match+=1
            elif student_subjects.get(sub,'') in ['C','D']:
                sub_match+=0.5
        sub_match*=15
        education_match = 20 if student['Educational_level'] == career['education_level'] else 0
        salarybias=career['Expected_Salary']/600000 *20
        
        X_pred.append([int_match, skill_match, sub_match, education_match,salarybias])
    
    scores = model.predict(X_pred)
    recommendations = [(career_paths[i], score) for i, score in enumerate(scores) if career_paths[i]['gender']==student['gender'] or career_paths[i]['gender']=='Any']
    recommendations.sort(key=lambda x: x[1], reverse=True)
    recommendations.sort(key=lambda x:x[0]['Expected_Salary'],reverse=True)
    recommendations.sort(key=lambda x:x[0]['locations'],reverse=True)
    for i in range(len(recommendations)-1):
        if recommendations[i][1] !=recommendations[i+1][1]:
            if i>=student['reqd']:
                print(f"We recommend looking at atleast {i+2} opportunities")
                break
    
    return recommendations

career_paths = read_json('career_path3.json')
student_data = read_json('student_data3.json')

X, y = prepare_data(career_paths, student_data)

model = train_regression_model(X, y)

rec_careers = recommend_careers(model, career_paths, student_data)
choice = student_data['Choice']
    
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
    if student_data['reqd']>=len(rec_careers):
        for career, score in rec_careers:
            print(career['career_name'])
    else:
        for i in range(student_data['reqd']):
            print(rec_careers[i][0]['career_name'],end=" - ")
            print(rec_careers[i][0]['locations'],end=", ")
            print(f"Expected Salary {rec_careers[i][0]['Expected_Salary']} Per Annum")


