'''
CS326 Lab 5
Author: D. Schuurman
Software PWM control of micro-servo motor position
'''
import RPi.GPIO as GPIO   # Import the GPIO library.
import time               # Import time library

# Constants
SERVO = 18                # Connect servomotor to BCM 18
PWM_FREQ = 50             # Set PWM frequency to 50Hz
DELAY = 2

GPIO.setmode(GPIO.BCM)      # Use BCM numbers
GPIO.setup(SERVO, GPIO.OUT) # Set SERVO pin to output mode.
pwm = GPIO.PWM(SERVO,PWM_FREQ)    

# loop through different angles
try:
   while True:
      print('setting angle = -72 degrees')
      pwm.start(5.5)
      time.sleep(DELAY)

      print('setting angle = 0 degrees')
      pwm.start(7.5)
      time.sleep(DELAY)

      print('setting angle = 72 degrees')
      pwm.start(9.5)
      time.sleep(DELAY)
 
except KeyboardInterrupt:
   # return to 0 degrees position and cleanup
   print('setting angle = 0 degrees')
   pwm.start(7.5)
   time.sleep(1) # Wait for servo to respond
   pwm.stop()
   GPIO.cleanup()
