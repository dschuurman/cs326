# CS326 Lab 7
# This program turns on an LED in response to an MQTT message.

from gpiozero import LED
import paho.mqtt.client as mqtt

# Constants
TOPIC = 'jcalvin/button'
PORT = 1883
QOS = 0
KEEPALIVE = 60

# setup LED on BCM 16
led = LED(16)

# Set hostname for MQTT broker
BROKER = ''

# Indicates whether broker requires authentication.
# Set to True for authenticaion, set to False for anonymous brokers
BROKER_AUTHENTICATION = True

# Note: these constants must be set if broker requires authentication
USERNAME = ''   # broker authentication username (if required)
PASSWORD = ''   # broker authentication password (if required)

# Callback when a connection has been established with the MQTT broker
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(f'Connected to {BROKER} successful.')
    else:
        print(f'Connection to {BROKER} failed. Return code={rc}')

# Callback when client receives a message from the broker
# Use button message to turn LED on/off
def on_message(client, data, msg):
    print(f'MQTT message received -> topic:{msg.topic}, message:{msg.payload}')
    if msg.topic == TOPIC:
       if led.is_lit
          led.off()
       else:
          led.on()

# Setup MQTT client and callbacks 
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

if BROKER_AUTHENTICATION:
    client.username_pw_set(USERNAME, password=PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker and subscribe to the button topic
client.connect(BROKER, PORT, KEEPALIVE)
client.subscribe(TOPIC, qos=QOS)

try:
    client.loop_forever()
except KeyboardInterrupt:
    client.disconnect()
    print('Done')
