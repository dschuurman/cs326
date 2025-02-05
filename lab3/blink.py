# CS326 Lab 3
# Blinking LED

from gpiozero import LED
import time

# Create LED object using GPIO pin 16
led = LED(16)
DELAY = 0.5

# Blink the LED 20 times
for count in range(20):
    led.on()
    print('LED: on')
    time.sleep(DELAY)
    led.off()
    print('LED: off')
    time.sleep(DELAY)

led.close()
print("Done!")