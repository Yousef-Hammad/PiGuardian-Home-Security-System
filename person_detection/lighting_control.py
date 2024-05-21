import time
import RPi.GPIO as GPIO # Provides access to GPIO pins
from gpiozero import LED # Used for controlling the LED

# Initialize the LED connected to GPIO pin 24
light = LED(24)

# Define the GPIO pin (18) connected to the photoresistor
photoresistor = 18 

# Set the GPIO mode to BCM to use Broadcom SOC channel numbers
GPIO.setmode(GPIO.BCM)

# Set up the photoresistor pin as an input
GPIO.setup(photoresistor, GPIO.IN)

def main():
    """
    Main function to control an LED based on the photoresistor input.
    
    Continuously checks the state of a photoresistor connected
    to a GPIO pin. If the photoresistor detects light, the
    LED is turned off. If it's dark, the LED turns on for a
    period of time before turning off again to simulate an automatic lighting
    system that responds to ambient light conditions.
    """
    while(True):
        if GPIO.input(photoresistor):
            # Light is detected
            print("Light is off because it is daytime")
            light.off()
        else:
            # Light is not detected
            print("Light is on because it is dark")
            light.on()
            time.sleep(3) # Keep LED on for 3 seconds
            light.off()
            time.sleep(5) # Wait for 5 seconds before next loop iteration to prevent immediate reactivation
                
        
if __name__ == '__main__':
        main()
