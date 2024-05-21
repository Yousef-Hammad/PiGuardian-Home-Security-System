import time
import board
import adafruit_vl53l1x as af

i2c = board.I2C()

# Create an instance of the VL53L1X sensor
vl53 = af.VL53L1X(i2c)
vl53.distance_mode = 2 # Set sensor to long distance mode (1 would set it to short mode)
vl53.timing_budget = 100 # Set the timing budget for measurements in milliseconds

vl53.start_ranging()

# Main loop to continuously check and print the distance measurement
while True:
    if vl53.data_ready:
        print("Distance: {} cm".format(vl53.distance))    
        vl53.clear_interrupt() # Clear the interrupt to prepare for the next measurement
        time.sleep(1.0)
