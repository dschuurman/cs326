'''
CS326 Lab 3
Author: D. Schuurman
Count the number of input switch transitions
'''
import RPi.GPIO as GPIO

GPIO12 = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
count=0
state = 1     # Keeps track of the last state of the input
try:
   while True:
      if GPIO.input(GPIO12)==False and state==1:
         count += 1
         print(count)
         state = 0
      if GPIO.input(GPIO12)==True and state==0:
         state = 1
except KeyboardInterrupt:
   GPIO.cleanup()
