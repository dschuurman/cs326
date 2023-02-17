'''
CS326 Lab 5
Author: D. Schuurman
Sample a PWM signal with an A/D converter
'''
import RPi.GPIO as GPIO
import signal
from datetime import datetime
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# Constants
SAMPLE_TIME = 0.010
A2D_CH0 = 0
FILENAME = 'datalog.csv'
PWM = 16             # PWM on BCM 16
PWM_FREQ = 1         # frequency=1HZ
PWM_DUTY_CYCLE = 50  # set duty cycle

# Start PWM at 1Hz and 50% duty cycle
GPIO.setmode(GPIO.BCM)         # Use BCM numbers
GPIO.setup(PWM, GPIO.OUT)      # Set pin to output mode.
pwm = GPIO.PWM(PWM, PWM_FREQ)  # Initialize PWM frequency
pwm.start(PWM_DUTY_CYCLE)      # Initialize duty cycle

# create A/D spi bus, chip select, and mcp object
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)

# create an analog input for CH0
chan = AnalogIn(mcp, MCP.P0)

# Open a data logging file
f = open(FILENAME,'w')

def handler(signum, frame):
    ''' Timer signal handler
    '''
    time = datetime.now().time()
    value = chan.value >> 6
    voltage = chan.voltage
    f.write(f'{time},{value},{voltage}\n')

# Setup interval timer signal every sample time
signal.signal(signal.SIGALRM, handler)
signal.setitimer(signal.ITIMER_REAL, 1, SAMPLE_TIME)
            
print('Press Ctrl-C to quit...')
try:
    while True:
        signal.pause()
except KeyboardInterrupt:
    signal.setitimer(signal.ITIMER_REAL, 0, 0)  # Cancel interval timer
    f.close()
    print('Done')
