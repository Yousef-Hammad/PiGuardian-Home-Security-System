from gpiozero import Button
import pyrebase


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

doorbell = Button(6)

while True:

    if doorbell.is_pressed:
        db.child("scanFace").set(True)