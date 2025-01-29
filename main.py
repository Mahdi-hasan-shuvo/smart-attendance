__Developer__="Mahdi Hasan Shuvo"
__GitHub__= "https://github.com/Mahdi-hasan-shuvo"
__Facebook__= 'https://www.facebook.com/bk4human'

# Importing Libraries
from mahdix import *
from face_recognition import face_locations, face_encodings, load_image_file,face_distance
import cv2
clear()
print("Welcome to Face Recognition System")
# Student data (name, image file, etc.)
data_student = [                  #  you add more students use database
    { "Name_name": "Mahdi Hasan",
      "S_symester": "1",
      "F_faculty": "CSE",
      "I_id": "2024-2028",
      "I_image": "me.PNG" },
    { "Name_name": "Rahul Hasan",
      "S_symester": "3",
      "F_faculty": "CSE",
      "I_id": "2024-2028",
      "I_image": "he.PNG" }
      ]
# Load the face encodings for each student image
loads_face = [face_encodings(load_image_file(data["I_image"]))[0] for data in data_student] 
__webvideo_path='PXL_20250117_083224374.mp4'
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
    frame_face_encoding= face_encodings(frame,frame_face_location,model='hog')
    for face_location, face_encoding in zip(frame_face_location, frame_face_encoding):
        top, right, bottom, left = face_location
        distances = face_distance(loads_face, face_encoding)
        best_match_index = distances.argmin()  # Find the closest match
        if distances[best_match_index] < 0.6:  # If the distance is less than 0.6, it's a match
            print(f"{LI_WHITE}Found match on frame {LI_YELLOW}{cap.get(cv2.CAP_PROP_FRAME_COUNT)} for student {LI_GREEN}{data_student[best_match_index]['Name_name']}")
            student_name = data_student[best_match_index]
            put_text=f'{student_name["Name_name"]}[{student_name["F_faculty"]}-{student_name["S_symester"]}]'
            cv2.putText(frame, str(student_name["I_id"]), (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            cv2.putText(frame, put_text, (left, top - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()




