# CS326 Lab 5
# Hardware PWM control of micro-servo motor position

import time 
import pigpio

# Constants
PWM = 18      # Use hardware PWM on BCM 18
DELAY = 2

pi = pigpio.pi()       # connect to the pigpio service
if not pi.connected:
   exit(0)
pi.set_PWM_frequency(PWM,50);  # Set PWM frequency to 50Hz

try:
   while True:
      print('setting angle = -72 degrees')
      pi.set_servo_pulsewidth(PWM, 1100)
      time.sleep(DELAY)

      print('setting angle = 0 degrees')
      pi.set_servo_pulsewidth(PWM, 1500)
      time.sleep(DELAY)

      print('setting angle = 72 degrees')
      pi.set_servo_pulsewidth(PWM, 1900)
      time.sleep(DELAY)
 
except KeyboardInterrupt:
   pi.set_servo_pulsewidth(PWM, 0)    # turn pulses off
   pi.stop()
