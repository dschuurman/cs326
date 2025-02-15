# CS326 Lab 5
# Software PWM control of micro-servo motor position

from gpiozero import Servo
import time

DELAY = 2

# Use the gpiozero Servo class
SERVO = Servo(18)  # Connect servomotor to BCM 18

try:
    while True:
        print('setting minimum angle...')
        SERVO.value = -1  # Equivalent to 5.5% duty cycle
        time.sleep(DELAY)
        
        print('centering...')
        SERVO.value = 0  # Equivalent to 7.5% duty cycle
        time.sleep(DELAY)
        
        print('setting maximum angle...')
        SERVO.value = 1  # Equivalent to 9.5% duty cycle
        time.sleep(DELAY)
        
except KeyboardInterrupt:
    # return to 0 degrees position before exiting
    print('Reset angle...')
    SERVO.value = 0
