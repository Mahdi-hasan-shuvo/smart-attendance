
__Developer__="Mahdi Hasan Shuvo"
__GitHub__= "https://github.com/Mahdi-hasan-shuvo"
__Facebook__= 'https://www.facebook.com/bk4human'
# Importing Libraries
# ! pip install deepface
# ! pip install face-recognition
# ! pip install mahdix
# ! pip install requests

from mahdix import *
from face_recognition import face_locations, face_encodings, load_image_file,face_distance
from datetime import datetime, timedelta
import cv2
from time import sleep
from threading import Thread
import requests  
from deepface import DeepFace
# from pymongo import MongoClient
# this is a online database use mongodb 
# connection_string = "mongodb+srv://test12345678:123@cluster0.5cc7yod.mongodb.net/"
# client = MongoClient(connection_string)
# db = client.Mahdi_panel
# panel_codes  = db["s_data"]
# student_data = panel_codes.find_one() # student data base


student_data=[ # this is a locall student database
    {"Name":"Mahdi Hasan" ,
    "S_ID":"101-215-030",
    "S_semester":"1",
    "Groups" : "CSE",
    "S_img": "students/me.PNG"
    },
    {"Name":"Didar Ahmed" ,
    "S_ID":"101-215-030",
    "S_semester":"1",
    "Groups" : "CSE",
    "S_img": "students/he.PNG"
    },
    {"Name":"Dulal Ahmed" ,
    "S_ID":"101-215-030",
    "S_semester":"1",
    "Groups" : "EEE",
    "S_img":"students/mama.PNG"
    },
]

attended_list=[] # Who are Attend
W_Attendance =[] # Who are Wrong attend in the other class
frame_counter =0
frame_fps=30
Class_analisis_data=[


] 







from deepface import DeepFace
def analisis_frame(frame,deparment):
    objs = DeepFace.analyze(
    img_path = frame,
    actions = [ 'emotion','gender'])
    for data in objs:
        print(data['dominant_emotion'])
        dominant_emotion = data['dominant_emotion']
        dominant_gender = data['dominant_gender']
        region=data['region']
        x=region['x']
        y=region['y']
        w=region['w']
        h=region['h']
        Class_analisis_data.append({"Class":deparment,
        "emotion":dominant_emotion,
        "gender": dominant_gender})
        print(Class_analisis_data)


# Load the face encodings for each student image
lods_file_conoding = [face_encodings(load_image_file(''+data["S_img"]))[0] for data in student_data]


__webvideo_path='G1.mp4'
# Load the video capture from the file
cap = cv2.VideoCapture(__webvideo_path)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
def sending_notifiction(append_list,notice=" Are Not Attendance",files = {'photo': None}): # sending the sms 
    for data in student_data:
        if data["Name"]  in append_list:
            TOKEN = '7604751682:AAGPgyEBB1Otnp8VqISjiU_MUvcxssJxGmY'  
            CHAT_ID = '1911135214'  
            MESSAGE = f'Name : {data["Name"]} \nID :{data['S_ID']}\n{notice}'  
            url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'  
            data = {  
                'chat_id': CHAT_ID,  
                'text': MESSAGE , }  
            response = requests.post(url, data=data,files=files)


def check_face(frame,class_room="R-1",Group="CSE"):
    frame_face_location= face_locations(frame,number_of_times_to_upsample=0,model='hog')
    frame_face_encoding= face_encodings(frame,frame_face_location,model='small')
    for face_location, face_encoding in zip(frame_face_location, frame_face_encoding):
        distances = face_distance(lods_file_conoding, face_encoding)
        # top, right, bottom, left = face_location # face location
        best_match_index = distances.argmin()  # Find the closest match
        if distances[best_match_index] < 0.6:  # If the distance is less than 0.6, it's a match
            student_name = student_data[best_match_index]
            if student_name["Groups"] in  Group:
                attended_list.append(student_name["Name"])
                print(f'\nStudent Name : {LI_GREEN}{student_name["Name"]}\nGroups : {LI_RED}{student_name["Groups"]}\nID : {LI_YELLOW}{student_name["S_ID"]}')
            else:
                W_Attendance.append(student_name["Name"])
                print(f'\nWrong Student Name : {LI_RED}{student_name["Name"]}\nGroups : {LI_RED}{student_name["Groups"]}\nID : {LI_YELLOW}{student_name["S_ID"]}')  



while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    frame_counter +=1
    if frame_counter % 20 == 0:
        try:
            trefds=Thread(target=check_face,args=(frame,))#.start()
            trefds.start()
        except:pass
    if frame_counter % frame_fps ==0:
        try:
            trefds=Thread(target=analisis_frame,args=(frame,"CSE",))#.start()
            trefds.start()
        except:pass

    # sleep(.05)
#     cv2.imshow('Video', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()






sending_notifiction([daia['Name'] for daia in student_data if daia['Name'] not in attended_list if daia['Name'] not in W_Attendance ]) # who are not attend
sending_notifiction(W_Attendance," Are Attendance In Wrong Calss")


# Class_analisis_data = [
#     {"Class": "CSE", "emotion": "HAHA", "gender": "Man"},
#     {"Class": "CSE", "emotion": "natural", "gender": "Man"},
#     {"Class": "CSE", "emotion": "sad", "gender": "Man"},
#     {"Class": "CSE", "emotion": "HAHA", "gender": "Female"},
#     {"Class": "CSE", "emotion": "angry", "gender": "Man"},
#     {"Class": "CSE", "emotion": "natural", "gender": "Female"}]


gender_count, emotion_count_by_gender = {"Man": 0, "Female": 0}, {"Man": {}, "Female": {}}
for entry in Class_analisis_data:
    gender, emotion = entry["gender"], entry["emotion"]
    gender_count[gender] += 1
    emotion_count_by_gender[gender][emotion] = emotion_count_by_gender[gender].get(emotion, 0) + 1
for gender, emotions in emotion_count_by_gender.items():
    print(f"\nGender: {gender}")
    for emotion, count in emotions.items():
        print(f"  Emotion: {emotion}, Percentage: {(count / gender_count[gender]) * 100:.2f}%")
