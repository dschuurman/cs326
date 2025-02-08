# CS326 Lab 9
# This program stores an I2C TC74 temperature sensor reading every 10 seconds to a PostgreSQL cloud database.

import smbus
import time
import sys
import signal
import urllib.parse as up
import psycopg2

# Constants
BUS = 1            # I2C bus number
ADDRESS = 0x48     # TC74 I2C bus address
TIMEZONE = "America/Detroit"
URI = 'postgres://username:password@hostname/database'  # cloud database URI
TABLE = 'temperaturedata'
PERIOD = 10

def timer_handler(signum, frame):
    ''' Periodic timer signal handler
    '''
    global bus
    global conn
    global cursor
    temp = bus.read_byte(ADDRESS)   # Read TC74 sensor
    # Insert data into database
    sqlcmd = f"INSERT INTO {TABLE} (temperature) VALUES ({temp})"
    cursor.execute(sqlcmd)
    print(sqlcmd)
    conn.commit()

# Connect to I2C bus
bus = smbus.SMBus(BUS)

# Connect to the SQL cloud database
up.uses_netloc.append("postgres")
uri = up.urlparse(URI)
conn = psycopg2.connect(database=uri.path[1:], user=uri.username, password=uri.password, host=uri.hostname, port=uri.port )

# Open a cursor to perform database operations
cursor = conn.cursor()

# Set the local timezone for this session
cursor.execute(f'SET TIME ZONE "{TIMEZONE}"')
conn.commit()

# Setup signal to call handler every PERIOD seconds
signal.signal(signal.SIGALRM, timer_handler)
signal.setitimer(signal.ITIMER_REAL, 1, PERIOD)

# Continuously loop blocking on signals
try:
    while True:
        signal.pause()  # block on signal

except KeyboardInterrupt:
    bus.close()
    signal.alarm(0)     # Cancel signal alarm
    conn.close()
    print('Done')
