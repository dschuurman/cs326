'''
CS326 Lab 4
Author: D. Schuurman
Program to continuously read A/D converter
'''
from time import sleep
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input for CH0
chan = AnalogIn(mcp, MCP.P0)

while True:
    print(f'Raw ADC Value:{chan.value>>6} Voltage:{chan.voltage} volts')
    sleep(0.1)
