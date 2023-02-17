'''
CS326 Lab 3
Author: D. Schuurman
Blinking LED
'''

import time
import RPi.GPIO as GPIO

GPIO16 = 16
DELAY = 0.5

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO16, GPIO.OUT)

for count in range(20):
    GPIO.output(GPIO16, True)
    print('LED: on')
    time.sleep(DELAY)
    print('LED: off')
    GPIO.output(GPIO16, False)
    time.sleep(DELAY)

print("Done!")
GPIO.cleanup()
