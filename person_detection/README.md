## Person Detection README
### Group number: L2-G6
### Student name: Alizee Drolet
___
1. **About**

   This directory handles the person_detection, proximity sensing, and lighting control of the project.

2. **Contents of Directory**
   - coco_labels.txt: text file that contains object dataset labels
   - end2end_test.py: end to end python test that tests sending the output of person_detection.py to the database
   - lighting_control.py: python script that controls the lighting of the LED on an external circuit
   - lighting_control_test.py: test class that validates the functionality of lighting_control.py
   - main_rpi.py: main python script that creates threads for lighting_control and person_detection (the main script that will keep running for the project)
   - mobilenet_v2.tflite: a tensorflow lite pretrained model that detects objects
   - person_detection.py: python script that detects people using the pi camera and records a video for 30 seconds
   - person_detection_test.py: test class that validates the functionality of person_detection.py
   - prox_sensor.py: python script that prints the distance that the proximity sensor detects
   - temp_label_file.txt: sample label file created by person_detection_test.py
   - test.mp4: video file created by person_detection.py

3. **To Run**
   - A circuit with an LED and a resistor needs to be created (with the correct pins in lighting_control.py) and connected to the Rasbperry Pi 4
   - If the VL53L1X proximity sensor is connected, run the script by entering the following command into the Linux terminal: python3 main_rpi.py
   - If the VL53L1X proximity sensor is not connected, run the script by entering the following command into the Linux terminal: python3 main_rpi.py --object
     - *make sure to uncomment a few lines at the bottom of the main_rpi.py script
   
