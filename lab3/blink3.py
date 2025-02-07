# CS326 Lab 3
# Blinking LED using blink method
from gpiozero import LED
import time

# Create LED object using GPIO pin 16
led = LED(16)
DELAY = 0.5

led.blink(DELAY,DELAY,20,False)

led.close()
print("Done!")