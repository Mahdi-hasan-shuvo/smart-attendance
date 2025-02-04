
# Importing Libraries
from mahdix import *
from face_recognition import face_locations, face_encodings, load_image_file,face_distance
from pymongo import MongoClient
from datetime import datetime, timedelta
import cv2

clear()
print("Welcome to Face Recognition System")
student_data=[
    {"Name":"Mahdi Hasan" ,
    "S_ID":"101-215-030",
    "S_semester":"1",
    "Groups" : "CSE",
    "S_img": "students\\me.PNG"
    },
    {"Name":"Didar Ahmed" ,
    "S_ID":"101-215-030",
    "S_semester":"1",
    "Groups" : "LLB",
    "S_img": "students\\he.PNG"
    },
    {"Name":"Dulal Ahmed" ,
    "S_ID":"101-215-030",
    "S_semester":"1",
    "Groups" : "CSE",
    "S_img":"students\\mama.PNG"
    },
]
lods_file_conoding= [face_encodings(load_image_file("F:\\VERCITY\\attandance\\" + data["S_img"]))   for data in student_data]
__webvideo_path=r'F:\VERCITY\attandance\G2.mp4'


def check_face(frame,class_room="G1",Group="CSE"):
    frame_face_location= face_locations(frame,model='hog')
    frame_face_encoding= face_encodings(frame,frame_face_location)
    for face_location, face_encoding in zip(frame_face_location, frame_face_encoding):
        top, right, bottom, left = face_location
        distances = face_distance(lods_file_conoding, face_encoding)
        print(distances)
        best_match_index = distances.argmin()  # Find the closest match
        print(best_match_index)
        if distances[best_match_index] < 0.6:  # If the distance is less than 0.6, it's a match
            print(f"{LI_WHITE}Found match on frame {LI_YELLOW} for student {LI_GREEN}{student_data[best_match_index]['Name']}")
            student_name = student_data[best_match_index]
            put_text=f'{student_name["Name"]}[{student_name["S_ID"]}-{student_name["Groups"]}]'
            print(put_text)





# Load the face encodings for each student image
# loads_face = [face_encodings(load_image_file("students\\"+data["I_image"]))[0] for data in data_student] 
__webvideo_path='G2.mp4'
# Load the video capture from the file
cap = cv2.VideoCapture(__webvideo_path)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

cv2.namedWindow('Video')
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    frame_face_location= face_locations(frame,model='hog')
    frame_face_encoding= face_encodings(frame,frame_face_location)
    for face_location, face_encoding in zip(frame_face_location, frame_face_encoding):
        top, right, bottom, left = face_location
        distances = face_distance(loads_face, face_encoding)
        best_match_index = distances.argmin()  # Find the closest match
        print(best_match_index)
        if distances[best_match_index] < 0.6:  # If the distance is less than 0.6, it's a match
            print(f"{LI_WHITE}Found match on frame {LI_YELLOW} for student {LI_GREEN}{student_data[best_match_index]['Name']}")
            student_name = data_student[best_match_index]
            put_text=f'{student_name["Name"]}[{student_name["Groups"]}-{student_name["S_ID"]}]'
            cv2.putText(frame, str(student_name["I_id"]), (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            cv2.putText(frame, put_text, (left, top - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()




