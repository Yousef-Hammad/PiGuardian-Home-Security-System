import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify, render_template
#from controller import add_user, login, get_videos, register_new_face
from controller import add_user, login, door_lock_status, set_register_boolean, get_videos
from database.firestore_client import get_user_attribute, get_user_names
from database.firebase import add_event
from flask_cors import CORS

import json
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore


CREDENTIALS = credentials.Certificate("/Users/youse/Desktop/Sysc 3010 GUI/serviceAccountKey.json")

# with open(CREDENTIALS, "r") as file:
#     config = json.load(file)
# firebase = pyrebase.initialize_app(config)
# db = firebase.database()


app = Flask(__name__)
CORS(app)



@app.route('/')
def indx():
    return render_template('index.html'), 200


@app.route('/register_user', methods=['POST'])
def register_user():
    #get user information
    name = request.form['name']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    
    # Attempt to add user
    try:
        add_user(name, username, email, password)
        return render_template('successfulRegistration.html'), 200
    except Exception as e:
        return render_template('error.html', message = "An error occured while trying to register the user, please try again."), 500
    

@app.route('/get_user_attributes/<username>/<attribute>', methods=['GET'])
def get_user_attributes_route(username, attribute):

    # Check if username and attribute are provided
    if not username or not attribute:
        return render_template('error.html', message = "username or attributed not provided"), 400

    user_attribute = get_user_attribute(username, attribute)
   

    if user_attribute is None:
        return render_template('error.html', message = "attribute provided is invalid, please try again"), 400

    # Return the user attribute
    return jsonify({attribute: user_attribute}), 200

@app.route('/add_event', methods=['POST'])
def add_event_route():
    data = request.json
    
    event_type = data.get('event_type')
    details = data.get('details')
    
    # Check if all required fields are provided
    
    if not event_type or not details:
        return jsonify({'error': 'Missing required field(s)'}), 400
    
    # Call the add_event function from firebase.py
    try:
        add_event(event_type,details)
        return jsonify({'message': 'Event added successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@app.route('/login', methods=['POST'])
def login_route():

    username = request.form['username']
    password = request.form['password']


    # Attempt to log in with username and password
    if login(username, password):
        return render_template('userHomePage.html', name=username), 200
    else:
        return render_template('error.html', message = "Invalid username or password. Please try again"), 400
    


@app.route('/view_recorded_videos', methods=['GET'])
def get_videos_for_user():
    video_urls = get_videos()  # Call the function once and store its result in a variable
    print(video_urls, "videos URLS")  # Debugging: Print the result to see if URLs are fetched correctly
    try:
        if video_urls:
            # Pass the video URLs to the template correctly
            return render_template('showVideos.html', video_urls=video_urls), 200
        else:
            # No videos found, or an empty list is returned
            return render_template('error.html', message="No videos found."), 404
    except Exception as e:
        print(e)  # Print the actual error message to the console for debugging
        return render_template('error.html', message="Error encountered while trying to get playback videos."), 400



@app.route('/register_face/<username>/', methods=['GET','POST'])
def register_face(username):

    # Attempt to register a new face
    try:
        set_register_boolean(username)
        #return "SUCCESS SETTTING"
        return render_template('registerFace.html'), 200
    except:
        return render_template('error.html', message = "Error encountered while trying to set registerFace boolean"), 400



@app.route('/register_face_screen', methods=['GET'])
def register_face_screen():

    # get user name to register the face with
    try:
        return render_template('register_face.html'), 200
    except:
        return render_template('error.html', message = "Error encountered while trying to navigate to the user registration page"), 400



@app.route('/door_lock_status', methods=['GET'])
def get_door_status():

    # Attempt to get door lock status
    try:
        status = door_lock_status()
        print(status)
        return render_template('lockStatus.html', status = status), 200
    except:
        return render_template('error.html', message = "Error encountered while trying to get the door lock status. please try again"), 400




if __name__ == "__main__":
    app.run(debug=True)    

    
