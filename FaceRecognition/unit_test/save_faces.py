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


def encode_known_face(known_face_path):
    global known_face_names
    name = "test"
    
    face_image = face_recognition.load_image_file(known_face_path) #Loads image as numpy array
    face_encoding = face_recognition.face_encodings(face_image)
    if face_encoding:
        face_encoding = face_recognition.face_encodings(face_image)[0]

        
        list_known_face_encodings = face_encoding.tolist()
        #db.child(username).child(dataset_encodings).child(name).set(list_known_face_encodings)
        
        #print("Face recognition passed for " + name + "!")
        return True
    else:
        #print("Face recognition failed for " + name + "!" + " Please retry with your full face in the picture.")
        return False


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

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480)}, lores={"size": (320, 240), "format": "YUV420"})
picam2.configure(config)


(w0, h0) = picam2.stream_configuration("main")["size"]
(w1, h1) = picam2.stream_configuration("lores")["size"]
s1 = picam2.stream_configuration("lores")["stride"]

faces = []
picam2.post_callback = draw_faces


known_faces_dir = "/home/bisher/face_recog_test/known_faces"
known_face_encodings = []
known_face_names = []

def main():
    name = str(input("What is your name? "))
    picam2.start_preview(Preview.QTGL)
    picam2.start()

    while True:
        
        buffer = picam2.capture_buffer("lores")
        grey = buffer[:s1 * h1].reshape((h1, s1))
        faces = face_detector.detectMultiScale(grey, 1.1, 3)
        if capture_needed:
            print("Face successfully detected, please stay still for 3 seconds!")
            time.sleep(3)
            known_face_path = os.path.join(known_faces_dir, name + ".jpg")
            picam2.capture_file(known_face_path)
            print("Facial Image has been taken, thanks " + name + "!")
            print("Image Test passed")
            capture_needed = False  # Reset flag after capturing
            picam2.stop_preview()
            encode_known_face(known_face_path)
            again = str(input("Would you like to retry or save a new face (y/n)? "))
            if again.upper() != 'Y':
                break    #
            name = str(input("What is your name? "))
            picam2.start_preview(Preview.QTGL)
            picam2.start()
    encode_known_face(known_face_path)

if __name__ == "__main__":
    main()