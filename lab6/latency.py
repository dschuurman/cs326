# CS326 Lab 6
# Experimentally record latency from GPIO event to callback function
from gpiozero import DigitalInputDevice, DigitalOutputDevice
import time

# Constants
COUNT = 5000  # Number of samples
HISTOGRAM_SIZE = 500
NANOSECS_PER_MICROSEC = 1000

# GPIO pin objects
pin = DigitalInputDevice(16)  # Input pin
pout = DigitalOutputDevice(18)  # Output pin

# Global variables for timing measurements
t1 = 0
sum_of_latencies = 0
max_latency = 0
histogram = [0] * HISTOGRAM_SIZE

# Callback function for input
def input_callback():
    global t1, max_latency, sum_of_latencies, histogram
    
    # record time elapsed and store
    latency = time.time_ns() - t1
    if latency > max_latency:
        max_latency = latency
    
    latency_in_microseconds = int(latency/NANOSECS_PER_MICROSEC)
    if latency_in_microseconds < HISTOGRAM_SIZE:
        histogram[latency_in_microseconds] += 1
    
    sum_of_latencies += latency

# Set up the input pin callback
pin.when_activated = input_callback

# Loop numerous times toggling output to trigger input event
for count in range(COUNT):
    t1 = time.time_ns()
    pout.on()  # equivalent to HIGH
    time.sleep(0.01)
    pout.off()  # equivalent to LOW

# Report measurements
print("Histogram of latencies measured:")
for x in range(len(histogram)):
    print(f'{x+1},{histogram[x]}')

print(f'Average latency: {(sum_of_latencies/COUNT)/NANOSECS_PER_MICROSEC} microseconds')
print(f'Maximum latency: {max_latency/NANOSECS_PER_MICROSEC} micro-seconds')
