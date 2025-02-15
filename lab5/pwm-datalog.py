# CS326 Lab 5
# Sample a PWM signal with an A/D converter

import signal
from gpiozero import PWMOutputDevice
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

# Start a PWM signal on BCM 16 at 1Hz and 50% duty cycle
pwm = PWMOutputDevice(pin=16,initial_value=0.5,frequency=1.0)

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
