'''
CS326 Lab 7
Author: D. Schuurman
This program sends an MQTT message whenever a button is pressed.
'''
import os
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

# Constants
PORT = 1883
QOS = 0
KEEPALIVE = 60
BUTTON = 12
BOUNCETIME = 500
TOPIC = 'jcalvin/button'
MESSAGE = 'Button pressed'

# Set hostname for MQTT broker
BROKER = ''

# Indicates whether broker requires authentication
# Set to True for authenticaion, set to False for anonymous brokers
BROKER_AUTHENTICATION = True

# Note: these constants must be set if broker requires authentication
USERNAME = ''   # broker authentication username
PASSWORD = ''   # broker authentication password

# Callback when a connection has been established with the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f'Connected to {BROKER} successful.')
    else:
        print(f'Connection to {BROKER} failed. Return code={rc}')

# Callback function when button is pressed
def button_callback(channel):
    global client 
    (result, num) = client.publish(TOPIC, MESSAGE, qos=QOS)
    if result == 0:
        print(f'MQTT message published -> topic:{TOPIC}, message:{MESSAGE}')
    else:
        print(f'PUBLISH returned error: {result}')

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)  

# Use GPIO 12 as button inputs
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

# Setup MQTT client and callbacks
client = mqtt.Client()
if BROKER_AUTHENTICATION:
    client.username_pw_set(USERNAME,password=PASSWORD)
client.on_connect=on_connect
client.connect(BROKER, PORT, KEEPALIVE)

# Detect a falling edge on input pin
GPIO.add_event_detect(BUTTON, GPIO.FALLING, callback=button_callback, bouncetime=BOUNCETIME)  

try:
    client.loop_forever()
except KeyboardInterrupt:
    client.disconnect()
    GPIO.cleanup()
    print('Done')
