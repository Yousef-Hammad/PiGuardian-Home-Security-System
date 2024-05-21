import threading
import time
import argparse
import board
import adafruit_vl53l1x as af
import person_detection as pd
import lighting_control as lc
import sys
from datetime import datetime
sys.path.insert(1, '/home/alizeedrolet/sysc3010-project-l2-g6/database')
from firebase import upload_file_to_storage

def main(object_detected = False):
    """
    Main function to control lighting and person detection.
    
    This function starts a thread for lighting control and continuously checks for the presence of
    an object. If an object is detected, it triggers person detection and uploads a video file
    to the database with a timestamp.
    
    Parameters:
    - object_detected (bool): Initial flag indicating if an object is detected. Defaults to False.
    """
    
    # Start a thread for lighting control so that it continuously runs    
    light_control_thread = threading.Thread(target=lc.main)
    light_control_thread.start()
    
    while(True):
        object_detected = prox_sensor()
        # Object detected so start thread to capture video
        if(object_detected == True):
            # When an object is detected by the sensor, create and start the person_detection thread
            person_detect_thread = threading.Thread(target=pd.main)
            person_detect_thread.start()
            
            # Send the video to the database with the timestamp as the name
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            filename = timestamp + '.mp4'
            upload_file_to_storage('/home/alizeedrolet/sysc3010-project-l2-g6/person_detection/test.mp4', filename)
    
            person_detect_thread.join()


def prox_sensor():
    """
    Checks for the presence of an object using the VL53L1X proximity sensor.
    
    This function creates an instance of the VL53L1X sensor, configures it for long distance
    mode and a specific timing budget, and continuously checks for object presence. If an object
    is detected within 3 meters, it returns True.
    
    Returns:
    bool: True if an object is detected within 3 meters, False otherwise.
    """
    
    i2c = board.I2C()
    vl53 = af.VL53L1X(i2c) # Create an instance of the VL53L1X sensor
    vl53.distance_mode = 2 # Set sensor to long distance mode (1 would set it to short mode)
    vl53.timing_budget = 100 # Set the timing budget for measurements in milliseconds

    vl53.start_ranging()
    
    # Main loop to continuously check and print the distance measurement
    while True:
        if vl53.data_ready:
            print("Distance: {} cm".format(vl53.distance))
            vl53.clear_interrupt() # Clear the interrupt to prepare for the next measurement
            time.sleep(1.0)
            
            # If an object is within 3m away from the sensor, return True
            if(vl53.distance < 300):
                return True
            
            
if __name__ == "__main__":
    '''
    # Manually trigger the code without the proximity sensor.
    # to run, enter the following command in the terminal: python3 main_rpi.py --object
    parser = argparse.ArgumentParser()
    parser.add_argument('--object', action="store_true", help='Specify if object is detected')
    
    args = parser.parse_args()
    
    main(args.object)
    '''
    main()
