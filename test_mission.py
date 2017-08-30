#!/usr/bin/env python

from __future__ import print_function
import time
import weather
import json
from dronekit import connect, VehicleMode, LocationGlobalRelative


# Set up option parsing to get connection string
import argparse
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None


# Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

@vehicle.on_message('DISARMING MOTORS')
def listener(self, name, message):
    print ("Disarm message callback activated!")
    print (message)


@vehicle.on_message('ARMING MOTORS')
def listener(self, name, message):
    print ("Arm message callback activated!")
    print (message)





def do_arm():
    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("We are armed!")

safe = False
backoff = 10

while not (safe):
    url = weather.buildUrlZip(2052, "au")
    data = weather.getWeather(url)
    print(json.dumps(data))
    if weather.checkWeather(data):
        do_arm()
        safe = True
    else:
        print("Weather is too dangerous checking again in: {0} seconds".format(backoff))
        #time.sleep(backoff)
        backoff = backoff * 2


while not False: time.sleep(0.1)

try:
    input("Press enter to continue...")
    print ("")
except SyntaxError:
    pass
