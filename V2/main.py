__Developer__="Mahdi Hasan Shuvo"
__GitHub__= "https://github.com/Mahdi-hasan-shuvo"
__Facebook__= 'https://www.facebook.com/bk4human'
# Importing Libraries
from mahdix import *
import face_recognition
from face_recognition import face_locations, face_encodings, load_image_file,face_distance
from datetime import datetime, timedelta
import cv2
from time import sleep
from threading import Thread
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


# Load the face encodings for each student image
lods_file_conoding = [face_encodings(load_image_file(data["S_img"]))[0] for data in student_data] 
__webvideo_path='G1.mp4'
# Load the video capture from the file
cap = cv2.VideoCapture(__webvideo_path)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
cv2.namedWindow('Video')


def check_face(frame,class_room="R-1",Group="CSE"):
    frame_face_location= face_locations(frame,model='hog')
    frame_face_encoding= face_encodings(frame,frame_face_location)
    for face_location, face_encoding in zip(frame_face_location, frame_face_encoding):
        top, right, bottom, left = face_location
        distances = face_distance(lods_file_conoding, face_encoding)
        best_match_index = distances.argmin()  # Find the closest match
        if distances[best_match_index] < 0.6:  # If the distance is less than 0.6, it's a match
            # print(f"{LI_WHITE}Found match on frame {LI_YELLOW} for student {LI_GREEN}{student_data[best_match_index]['Name']}")
            student_name = student_data[best_match_index]
            put_text=f'{student_name["Name"]}[{student_name["Groups"]}-{student_name["S_ID"]}]'
            print(f'Student Name : {LI_GREEN}{student_name["Name"]}\nGroups : {LI_WHITE}{student_name["Groups"]}\nID : {LI_YELLOW}{student_name["S_ID"]}')
    




counter =0 
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    counter +=1
    if counter % 30 == 0:
        try:
            Thread(target=check_face,args=(frame,)).start()
        except:pass
    sleep(.1)
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()




