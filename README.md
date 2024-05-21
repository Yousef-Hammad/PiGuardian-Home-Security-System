[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/5bxZGXM7)
### README
### PiGuardian Project (SYSC 3010)
### Group number: L2-G6
### Students: Bisher Abou-Alwan, Hamdiata Diakite, Alizée Drolet, Yousef Hammad
### TA: Oly Papillon

![frontImg](https://github.com/SYSC3010-W24/sysc3010-project-l2-g6/assets/91440838/f67d83c3-db14-499f-af1a-356b5bb97110)

___
**About**

PiGuardian aimed to boost the uptake of home security systems through the development of an advanced solution aimed at bolstering protection against intrusions. Using 4 Raspberry Pi computers, Our system sought to minimize vulnerabilities to burglaries and unauthorized entries by promptly notifying homeowners and supplying video recordings of entry points.

**Directory Map**
   - Demo:
      - This directory contains a file that was used for the end-end demo.
      - The file makes a POST and GET request and checks if the info save and the info recevied 
   - FaceRecognition:
     - This directory represents the facial recognition component needed to detect, scan, and encode a face.
     - It also handles the local database by calling local_database.py function implcitly from facial_recognition.py to update DB
     - The directory also includes the doorbell.py code to handle doorbell requests to scan a face
     - This contains a unit_test sub directory that provides a thorough functonal test to each method
   - Notification:
        - This directory contains file that handles the email noticiation system.
        - The file notifcations.py file contains a single function that sends a email from the piguardian email we created.
   - WeeklyUpdates:
     - This directory includes weekly individual reports from week 3 to week 12 of the course.
   - api:
     - This directory is split up into 2 main parts: backend and frontend.
     - The backend part contains the script controller.py which is used to communicate with the firebase data to pull and push data from there.
     - The frontend part contains the script route.py which is the main python script that will be used for the GUI. This script contains all the HTTP endpoints for the GUI.
     - This folder also contains the subfolders 'static' and 'templates.' These folders contain all the .html and .css code used to build the front of the GUI 
   - database:
     - This directory is used for all communication with the database.
     - The script firestore_client.py contains all the functions necessary to to extract and put data from the firebase such as getting user attributes, adding data, and much more.
     - The script firebase.py is also similar to the firestore_client.py script except that this one only deals with the real-time database. This script is used to extract the door lock information, and registering faces. Both these functions deal with the real-time database. 
   - person_detection
     - This directory handles the person_detection, proximity sensing, and lighting control of the project.
     - Includes test code for end to end testing, person detection testing, and lighting control testing.

**Installation Instructions**
   - Please install the following libraries and dependencies:
     - To install Pyrebase: 'pip3 install pyrebase'
     - To install OpenCV: 'pip3 install opencv-python'
     - To install Facial Recognition: 'pip3 install facial_recognition-python'
     - To install Numpy: 'pip3 install numpy'
     - To install SQLite3: 'sudo apt-get install sqlite3'
     - To install firebase_admin: 'pip3 install firebase_admin'
     - To install flask: 'pip3 install flask'
     - To install flask_cors: 'pip3 install flask_cors'
     - To install TensorFlow Lite: python3 -m pip install tflite-runtime
     - To install PiCamera2: apt install -y python3-picamera2
       

**How to run**
   - To run Facial Recognition node:
     - Firstly, hook up the PiCamera2 module on your RaspberryPi board. Next, connect the GPIO breakout board to your Raspberry Pi 4 and to the breadboard. Now we can circuit the doorbell by creating a series circuit comprising of the button and a resistor and lastly connecting to pin 6 on the breakout board via male-to-male cable. Once connected, we can launch our code files and run doorbell.py to activate the doorbell function and run facial_recognition.py to activate our facial recognition component, the local_database.py is called implicitly from facial_recognition.py so we need not worry about that.
   - To run the graphical user interface (GUI):
     - Running the GUI is relatilvey simple if you have everything installed and ready to go on your computer. Firstly make sure you have the entire project folder downloaded on your computer. Next, navigate to the route.py script inside the api folder and run the script. You should not encounter any issues if you have all the required installs (mentioned above) on your computer. Everything is good to go now, navigate to any browser and type localhost:5000 or 127.0.0.1:5000 to view the GUI. Please note that the GUI is only available on your local host machine.
   - To run the Person Detection and Lighting Control node:
     - First, construct the circuit with the proximity sensor and the photoresistor with the breakout board. The pins are indicated in the lighting_control.py module. Make sure to connect your Pi Camera to the Raspberry Pi and boot your Pi. Download all the required libraries and packages and run main_rpi.py.  

**Validate Installation**
   - To validate installations, please follow 2 stages. Stage 1 represents the unit tests, please run each node's unit test and verify that all tests pass. Stage 2    represents real-time functionality where we exercise the system, please register a user on the GUI, register a face, verify the door lock status, initiate a scan using the doorbell by scanning an unregistered face to verify status remains locked, initiate a second scan using the doorbell by scanning an registered face to verify status becomes unlocked, provide motion in front of the proximity sensors and verify motion detection videos are uploaded on the GUI, and lastly provide darkness above the light sensory to verify the LED turns on upon detecting darkness.
   
