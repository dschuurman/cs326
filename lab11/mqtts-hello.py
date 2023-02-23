'''
CS326 Lab 11
Author: D. Schuurman
Send periodic secure MQTT traffic.
'''
import paho.mqtt.client as mqtt
import time
import os

# Constants
PORT = 8883       # secure MQTT port
QOS = 0
DELAY = 5.0
TOPIC = 'cs326/jcalvin'
CERTS = '/etc/ssl/certs/ca-certificates.crt'

# Set hostname for MQTT broker
BROKER = ''

# Note: these constants must be set for broker authentication
USERNAME = ''   # broker authentication username
PASSWORD = ''   # broker authentication password

# Callback when a connection has been established with the MQTT broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f'Connected to {BROKER}')
    else:
        print('Connection to {BROKER} failed. Return code={rc}')
        os._exit(1)
   
# Setup MQTT client and callbacks
client = mqtt.Client()
client.on_connect = on_connect

# Securely connect to MQTT broker
client.username_pw_set(USERNAME, password=PASSWORD)
client.tls_set(CERTS)
client.connect(BROKER, PORT, 60)
client.loop_start()

# Continuously publish message
try:
    while True:
        print('publishing MQTTS message')
        client.publish(TOPIC, 'hello world')
        time.sleep(DELAY)

except KeyboardInterrupt:
    print('Done')
    client.disconnect()
