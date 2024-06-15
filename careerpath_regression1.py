import json
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def prepare_data(career_paths, student):
        X = []
        y = []
    
    
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
            if career['economic']>student['economical_status']:
                sub_match+=(student['economical_status']-career['economic'])*10
            else:
                sub_match+= (student['economical_status']-1)*10
            
            score = (int_match + skill_match + sub_match) /(len(career_interests)*15+len(career_skills)*15+len(career_subjects)*15) * 100
            
            X.append([int_match, skill_match, sub_match])
            y.append(score)
    
        return X, y

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
        if career['economic']>student['economical_status']:
            sub_match+=(student['economical_status']-career['economic'])*10
        else:
            sub_match+= (student['economical_status']-1)*10
        X_pred.append([int_match, skill_match, sub_match])
    
    scores = model.predict(X_pred)
    recommendations = [(career_paths[i]['career_name'], score) for i, score in enumerate(scores) if score >=0]
    recommendations.sort(key=lambda x: x[1], reverse=True)
    
    return recommendations

career_paths = read_json('career_path1.json')
student_data = read_json('student_data1.json')

X, y = prepare_data(career_paths, student_data)

model = train_regression_model(X, y)

rec_careers = recommend_careers(model, career_paths, student_data)
if len(rec_careers)>=student_data['reqd']:
    for career, score in rec_careers:
        print(career)
else:
    for i in range(len(rec_careers)):
        print(rec_careers[i][1])

