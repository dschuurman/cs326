'''
CS326 Lab 6
Author: D. Schuurman
Experimentally record latency from GPIO event to callback function
'''
import RPi.GPIO as GPIO
import time

# Constants
PIN = 16            # Input pin
POUT = 18           # Output pin
COUNT = 5000        # Number of samples
HISTOGRAM_SIZE = 500
NANOSECS_PER_MICROSEC = 1000

# Global variables are normally discouraged but used here so that
# timing variables are visible in main program and callback function
t1 = 0
sum_of_latencies = 0
max_latency = 0
histogram = [0] * HISTOGRAM_SIZE

# Initialize GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)
GPIO.setup(POUT, GPIO.OUT)
GPIO.output(POUT, GPIO.LOW)

# Callback function for input
def input_callback(channel):
   global t1
   global max_latency
   global sum_of_latencies
   global histogram

   # record time elapsed and store 
   latency = time.time_ns() - t1
   if latency > max_latency:
       max_latency = latency
   latency_in_microseconds = int(latency/NANOSECS_PER_MICROSEC)
   if latency_in_microseconds < HISTOGRAM_SIZE:
       histogram[latency_in_microseconds] += 1
   sum_of_latencies += latency


# Detect rising edges on the input pin
GPIO.add_event_detect(PIN, GPIO.RISING, callback=input_callback)

# Loop numerous times toggling output to trigger input event
for count in range(COUNT):
    t1 = time.time_ns()
    GPIO.output(POUT, GPIO.HIGH)
    time.sleep(0.01)
    GPIO.output(POUT, GPIO.LOW)

# Report measurements
print("Histogram of latencies measured:")
for x in range(len(histogram)):
    print(f'{x+1},{histogram[x]}')

print(f'Average latency: {(sum_of_latencies/COUNT)/NANOSECS_PER_MICROSEC} microseconds')
print(f'Maximum latency: {max_latency/NANOSECS_PER_MICROSEC} micro-seconds')

GPIO.cleanup()       # clean up GPIO

