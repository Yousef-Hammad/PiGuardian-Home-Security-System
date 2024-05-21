#!/usr/bin/python3
import time
import cv2
import face_recognition
from picamera2 import MappedArray, Picamera2, Preview
import numpy as np
import os
import pyrebase 

def draw_faces(request):
    global capture_needed
    with MappedArray(request, "main") as m:
        for f in faces:
            (x, y, w, h) = [c * n // d for c, n, d in zip(f, (w0, h0) * 2, (w1, h1) * 2)]
            cv2.rectangle(m.array, (x, y), (x + w, y + h), (0, 255, 0, 0))
            capture_needed = True

def retrieve_known_names():
    global known_face_names
    
    # Retrieve face encodings and names from Firebase
    face_encodings_data = db.child(username).child(dataset_encodings).get()

    # Check if the retrieval was successful
    if face_encodings_data.each() is not None:
        for item in face_encodings_data.each():
            name = item.key()  # The name of the individual
            known_face_names.append(name)
        return True
    return False
            
            
def retrieve_known_encodings():
    global known_face_encodings
    
    # Retrieve face encodings and names from Firebase
    face_encodings_data = db.child(username).child(dataset_encodings).get()

    # Check if the retrieval was successful
    if face_encodings_data.each() is not None:
        for item in face_encodings_data.each():
            encoding = np.array(item.val())  # Convert the list back into a NumPy array
            known_face_encodings.append(encoding)
        return True
    return False
    
def encode_unknown_face(unknown_image_path):
    unknown_image = face_recognition.load_image_file(unknown_image_path)
    unknown_face_encoding = face_recognition.face_encodings(unknown_image)
    if unknown_face_encoding:
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
        return unknown_face_encoding
    else:
        return None
        

###################################################################################################################

                                    #############FIREBASE INFO####################
config = { 
  "apiKey": "AIzaSyA38xl73beUZ1PJkbJvrBq9pJlobgEhEig", 
  "authDomain": "piguardian-bdb7e.firebaseapp.com", 
  "databaseURL": "https://piguardian-bdb7e-default-rtdb.firebaseio.com/", 
  "storageBucket": "piguardian-bdb7e.appspot.com" 
}

# Connect using the configuration 
firebase = pyrebase.initialize_app(config) 
db = firebase.database() 
dataset_encodings = "Known Face Encodings"
dataset_names = "Known Faces Names"
username = "Facial Recognition Camera"

###################################################################################################################


face_detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")


capture_needed = False  # Flag to indicate when a photo capture is needed

known_face_encodings = []
known_face_names = []



known_faces_dir = "/home/bisher/face_recog_test/known_faces"
known_face_encodings = []
known_face_names = []

def compare(unknown_img):
    unknown_face_encoding = encode_unknown_face(unknown_img)
    retrieve_known_names()
    retrieve_known_encodings()
    
    if unknown_face_encoding is not None:
        distances = face_recognition.face_distance(known_face_encodings, unknown_face_encoding)
        best_match_index = np.argmin(distances)
        if distances[best_match_index] < 0.6:  # Threshold for "closeness"
            print(f"Match found: {known_face_names[best_match_index]}")
            db.child("doorStatus").set(True)
        return True
    
    return False
    


##############retrieve_known_names()
##############retrieve_known_encodings()
def main():
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"size": (640, 480)}, lores={"size": (320, 240), "format": "YUV420"})
    picam2.configure(config)


    (w0, h0) = picam2.stream_configuration("main")["size"]
    (w1, h1) = picam2.stream_configuration("lores")["size"]
    s1 = picam2.stream_configuration("lores")["stride"]

    faces = []
    picam2.post_callback = draw_faces

    picam2.start_preview(Preview.QTGL)
    picam2.start()
        
    while True:
        buffer = picam2.capture_buffer("lores")
        grey = buffer[:s1 * h1].reshape((h1, s1))
        faces = face_detector.detectMultiScale(grey, 1.1, 3)
        if capture_needed:
            print("Face successfully detected, please stay still for 3 seconds!")
            time.sleep(3)
            picam2.capture_file("unknown_person.jpg")
            print("Face was detected, thanks!")
            capture_needed = False  # Reset flag after capturing
            picam2.stop_preview()
            break

    unknown_face_encoding = encode_unknown_face()
    if unknown_face_encoding is not None:
        distances = face_recognition.face_distance(known_face_encodings, unknown_face_encoding)
        best_match_index = np.argmin(distances)
        if distances[best_match_index] < 0.6:  # Threshold for "closeness"
            print(f"Match found: {known_face_names[best_match_index]}")
            db.child("doorStatus").set(True)
            print("TEST PASSED")
        else:
            print("No matching face found.")
    else:
        print("No matching face found.")


if __name__ == "__main__":
    main()