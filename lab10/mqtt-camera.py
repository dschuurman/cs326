'''
CS326 Lab 10
Author: D. Schuurman
MQTT motion detector using pi camera.
'''
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import sys
import cv2

# Constants
MOTION_THRESHOLD = 1000000
PORT = 8883
QOS = 0
LED = 16
DELAY = 2.0
CERTS = '/etc/ssl/certs/ca-certificates.crt'

# Set hostname for MQTT broker
BROKER = ''

# Note: these constants must be set for broker authentication
USERNAME = ''   # broker authentication username
PASSWORD = ''   # broker authentication password

def get_frame(cap):
    ''' Return grayscale image from camera
    '''
    ret = False
    ret, frame = cap.read()
    if not ret:
        print('Frame capture failed...')
        sys.exit(1)    
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

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
    ''' Callback when client receives a PUBLISH message from the broker
    '''
    if msg.topic == 'jcalvin/LED':
        print(f'Received message: LED = {msg.payload}')
        if int(msg.payload) == 1:
            GPIO.output(LED, True)
        elif int(msg.payload) == 0:
            GPIO.output(LED, False)

# Initialize camera
print('Initializing camera...')
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print('Cannot open camera...')
    sys.exit(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 2)

# Initialize GPIO LED output
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)

# Setup MQTT client and callbacks
client = mqtt.Client()
client.username_pw_set(USERNAME,password=PASSWORD) # remove for anonymous access
client.tls_set(CERTS)
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

# Connect to MQTT broker and subscribe to the button topic
client.connect(BROKER, PORT, 60)
client.subscribe("jcalvin/LED", qos=QOS)
client.loop_start()

# initialize background image and initialize motion state
last_frame = get_frame(cap)
motion_state = 0

try:
    while True:
        # grab a frame; compute abs difference from the last frame
        current_frame = get_frame(cap)
        frameDelta = cv2.absdiff(current_frame, last_frame)
        diff = frameDelta.sum()

        # If diff > threshold and state changes publish motion event
        if diff > MOTION_THRESHOLD:
            if motion_state == 0:
                print('motion detected!')
                client.publish('jcalvin/motion', '1')
                motion_state = 1
                time.sleep(DELAY)
                current_frame = get_frame(cap)  # after delay, refresh current frame
        else:
            if motion_state == 1:
                print('motion stopped...')
                client.publish('jcalvin/motion', '0')
                motion_state = 0

        # Update last_frame
        last_frame = current_frame

except KeyboardInterrupt:
    GPIO.cleanup()
    client.disconnect()
    cap.release()
    print('Done')
