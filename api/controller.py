import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from database.firestore_client import add_data_to_firestore, get_user_from_firestore, get_user_attribute, get_user_videos
from database.firebase import get_door_status, set_register_face


def add_user(name: str, username: str, email: str, password: str):
    '''
    Function to add user to the 'Users' collection in the firestore. 
    Parameters: 
        name: Name of the user to be added 
        username: Username of the user to be added 
        email: email if the user to be added
        phone: Phone number of rhe user to be added 
        password: Password of the email to be added
    '''
    user_info = {
        'name': name,
        'username': username,
        'email': email,
        'password': password
    }
    
    # Call function from Firebases to add user with username as doc id
    add_data_to_firestore('Users',user_info,username)
    
def login(username: str, password: str) -> bool:
        
    user_data = get_user_from_firestore(username)
    
    if user_data is not None:
        #Get password stored in firebase
        user_password = get_user_attribute(username,'password')
        # Check to see if stored password and password enters match
        if user_password == password:
            return True
        
        else:
            return False
    else:
        return False
    

def door_lock_status():
    return get_door_status()

def set_register_boolean(username):
    try:
        return set_register_face(username)
    except:
        print("Encountered error while trying to set to registerFace boolean to true")
        
        

def get_videos():
    try:
        return get_user_videos()
    except:
        print("Encountered error while trying to set to registerFace boolean to true")
        
        