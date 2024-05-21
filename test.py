import pyrebase
from datetime import datetime
import time

from sense_hat import SenseHat

sense = SenseHat()


config = { 
  "apiKey": "AIzaSyA38xl73beUZ1PJkbJvrBq9pJlobgEhEig", 
  "authDomain": "piguardian-bdb7e.firebaseapp.com", 
  "databaseURL": "https://piguardian-bdb7e-default-rtdb.firebaseio.com/", 
  "storageBucket": "piguardian-bdb7e.appspot.com" 
} 

# Initialize Pyrebase app
firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Function to change the Sense HAT LED matrix color
def update_led_matrix(is_locked):
    if not is_locked:
        # Set LEDs to red for locked
        sense.clear((255, 0, 0))
    else:
        # Set LEDs to green for unlocked
        sense.clear((0, 255, 0))
        time.sleep(5)
        db.child("doorStatus").set(False)

# Stream handler function
def stream_handler(message):
    print("Event type: {}".format(message["event"]))  # put
    print("Path: {}".format(message["path"]))  # /-K7yGTTEp7O549EzTYtI
    print("Data: {}".format(message["data"]))  # {'title': 'Pyrebase', 'body': 'etc...'}

    # Assuming message["data"] is a boolean indicating lock status
    update_led_matrix(message["data"])

# Start the stream
my_stream = db.child("doorStatus").stream(stream_handler)

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Stopping the stream...")
    my_stream.close()
    

    
