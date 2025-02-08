# CS326 Lab 10
# Web-of-Things AprilTag detector and LED controller using MQTT

import paho.mqtt.client as mqtt
from gpiozero import LED
import time
import sys
import cv2
from picamera2 import Picamera2
from pupil_apriltags import Detector

# Constants
PORT = 8883
QOS = 0
CERTS = '/etc/ssl/certs/ca-certificates.crt'

# Set hostname for MQTT broker
BROKER = ''

# Note: these constants must be set for broker authentication
USERNAME = ''   # broker authentication username
PASSWORD = ''   # broker authentication password

# define LED on BCM 16
led = LED(16)

def on_publish(client, userdata, mid):
    ''' Callback when an MQTT message is published
    '''
    print("MQTT data published")

def on_connect(client, userdata, flags, rc):
    ''' Callback when connecting to the MQTT broker
    '''
    if rc==0:
        print(f'Connected to {BROKER}')
    else:
        print(f'Connection to {BROKER} failed. Return code={rc}')
        sys.exit(1)

def on_message(client, data, msg):
    ''' Callback when client receives a subscribed message from the broker
        If LED message received, set LED on or off
    '''
    global led
    if msg.topic == 'jcalvin/LED':
        print(f'Received message: LED = {msg.payload}')
        if int(msg.payload) == 1:
            led.on()
        elif int(msg.payload) == 0:
            led.off()

# Initialize camera
print("Initializing camera...")
picam2 = Picamera2()
config = picam2.create_still_configuration( )
picam2.configure(config)
picam2.start()

# Setup MQTT client and callbacks
client = mqtt.Client()
client.username_pw_set(USERNAME,password=PASSWORD) # remove for anonymous access
client.tls_set(CERTS)
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

# Connect to MQTT broker and subscribe to the LED topic
client.connect(BROKER, PORT, 60)
client.subscribe("jcalvin/LED", qos=QOS)
client.loop_start()

# initialize AprilTag detector and state variable
detector = Detector()
tags_state = ''

try:
    while True:
        # grab a new frame and convert to grayscale
        frame = picam2.capture_array()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect any AprilTags
        results = detector.detect(img)

        # If state of tags has changed, publish an update
        if results == []:
            if tags_state != 'None':
                print('No tags found...')
                client.publish('jcalvin/tag', 'No tags found')
                tags_state = 'None'
        else:
            # Grab all tags detected
            tags = ''
            for r in results:
                # Print tag detection details
                print(f"AprilTag detected! ID: {r.tag_id}, Family: {r.tag_family}," f"Decision Margin: {r.decision_margin:.2f}")                
                tags += f'Tag:{r.tag_family}:{r.tag_id} '
            # If tags state has changes, publish a new message
            if tags != tags_state:
                client.publish('jcalvin/tag', tags)
                tags_state = tags

except KeyboardInterrupt:
    GPIO.cleanup()
    client.disconnect()
    picam2.stop()
    print('Done')
