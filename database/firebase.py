import pyrebase
from datetime import datetime


config = { 
  "apiKey": "AIzaSyA38xl73beUZ1PJkbJvrBq9pJlobgEhEig", 
  "authDomain": "piguardian-bdb7e.firebaseapp.com", 
  "databaseURL": "https://piguardian-bdb7e-default-rtdb.firebaseio.com/", 
  "storageBucket": "piguardian-bdb7e.appspot.com" 
} 

# Connect using your configuration 
firebase = pyrebase.initialize_app(config) 
db = firebase.database() 
storage = firebase.storage()  # Initialize Firebase storage


def add_event(event_type: str, details: dict):
  '''
  Function that add events to the firebase
  
  Paramaters:
    event_type: String that describes the type of event. 
    details: Additional details about the event in question 
  
  Returns: 
    None

  '''
  
  now = datetime.now()
  

  # Format as a string, if desired
  timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
  
 
  event_data = {
    'event_type' : event_type,
    'time':timestamp_str,
    'details':details
   
  }
  new_event = db.child('Events').push(event_data)
  
  
  
def upload_file_to_storage(file_path, file_name):
    '''
    Function to upload a file to Firebase Cloud Storage
    
    Parameters:
      file_path: Local path to the file
      file_name: Name to be used when storing the file in Firebase Storage
      
    Returns:
      URL of the uploaded file
    '''
    
    # Upload the file
    storage.child(file_name).put(file_path)
    
    # Get the URL of the uploaded file
    file_url = storage.child(file_name).get_url(None)
    
    return file_url 





def add_event(event_type: str, details: dict):
  '''
  Function that add events to the firebase
  
  Paramaters:
    event_type: String that describes the type of event. 
    details: Additional details about the event in question 
  
  Returns: 
    None

  '''
  
  now = datetime.now()
  

  # Format as a string, if desired
  timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
  
 
  event_data = {
    'event_type' : event_type,
    'time':timestamp_str,
    'details':details
   
  }
  new_event = db.child('Events').push(event_data)



def get_door_status():
    '''
    Function that retrieves the door status from the Firebase Realtime Database
    
    Returns:
        doorStatus (bool): The current status of the door (True for open, False for closed)
    '''
    try:
        doorStatus = db.child("doorStatus").get().val()
        return doorStatus
    except Exception as error:
        print(f"Error retrieving door status: {error}")
        return None
    

def set_register_face(username):
    '''
    Function to set the "registerFace" variable in Firebase Realtime Database to True.

    Returns:
        None
    '''
    try:
        db.child("registerFace").set(True)
        db.child("nameRequest").set(username)
        print("Successfully set registerFace to True")
    except Exception as error:
        print(f"Error setting registerFace: {error}")
