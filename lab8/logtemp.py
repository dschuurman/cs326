# CS326 Lab 8
# This program stores an I2C TC74 temperature sensor reading every 10 seconds to an SQLite database.

import smbus
import sqlite3
import time
import sys
import signal

# Constants
BUS = 1            # I2C bus number
ADDRESS = 0x48     # TC74 I2C bus address
FILENAME = 'temperature.db'  # SQLite filename
TABLE = 'temperaturedata'    # SQLite table name
PERIOD = 10.0                # Sample period (seconds)

def timer_handler(signum, frame):
    ''' Periodic timer signal handler
    '''
    global bus
    global db
    global cursor
    temp = bus.read_byte(ADDRESS)   # Read TC74 sensor
    # Insert data into database
    sqlcmd = f"INSERT INTO {TABLE} VALUES (datetime('now','localtime'),{temp})"
    cursor.execute(sqlcmd)
    db.commit()

# Connect to I2C bus
bus = smbus.SMBus(BUS)

# Connect to the database
db = sqlite3.connect(FILENAME)
cursor = db.cursor()

# Setup signal to call handler every PERIOD seconds
signal.signal(signal.SIGALRM, timer_handler)
signal.setitimer(signal.ITIMER_REAL, 1, PERIOD)

# Continuously loop blocking on signals
try:
    while True:
        signal.pause()      # block on signal
except KeyboardInterrupt:
    bus.close()
    db.close()
    print('Done')
