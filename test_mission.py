#!/usr/bin/env python

from __future__ import print_function
import time
import weather
import json
import math
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, mavutil
import wifi_module
import slant


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
vehicle = connect(connection_string, wait_ready=True, baud=57600, heartbeat_timeout=120)

'''
while True:
    print("Loop: %s" % str(vehicle.last_heartbeat))
    time.sleep(1)
'''
#time.sleep(10)

@vehicle.on_message('DISARMING MOTORS')
def listener(self, name, message):
    print ("Disarm message callback activated!")
    print (message)


@vehicle.on_message('ARMING MOTORS')
def listener(self, name, message):
    print ("Arm message callback activated!")
    print (message)

def upload_mission(aFileName):
    """
    Upload a mission from a file.
    """
    # Read mission from file
    missionlist = readmission(aFileName)

    print("\nUpload mission from a file: %s" % aFileName)
    # Clear existing mission from vehicle
    print(' Clear mission')
    cmds = vehicle.commands
    cmds.clear()
    #cmd = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
    #              mavutil.mavlink.MAV_CMD_MISSION_START, 0, 0, 0, 0, 0, 0, -34.364114, 149.166022, 30)

    #cmds.add(cmd)
    # Add new mission to vehicle
    for command in missionlist:
        cmds.add(command)
    print(' Upload mission')
    vehicle.commands.upload()

def readmission(aFileName):
    """
    Load a mission from a file into a list.

    This function is used by upload_mission().
    """
    print("Reading mission from file: %s\n" % aFileName)
    cmds = vehicle.commands
    missionlist=[]
    with open(aFileName) as f:
        for i, line in enumerate(f):
            if i==0:
                if not line.startswith('QGC WPL 110'):
                    raise Exception('File is not supported WP version')
            else:
                linearray=line.split('\t')
                ln_index=int(linearray[0])
                ln_currentwp=int(linearray[1])
                ln_frame=int(linearray[2])
                ln_command=int(linearray[3])
                ln_param1=float(linearray[4])
                ln_param2=float(linearray[5])
                ln_param3=float(linearray[6])
                ln_param4=float(linearray[7])
                ln_param5=float(linearray[8])
                ln_param6=float(linearray[9])
                ln_param7=float(linearray[10])
                ln_autocontinue=int(linearray[11].strip())
                cmd = Command( 0, 0, 0, ln_frame, ln_command, ln_currentwp, ln_autocontinue, ln_param1, ln_param2, ln_param3, ln_param4, ln_param5, ln_param6, ln_param7)
                missionlist.append(cmd)
    return missionlist

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
    vehicle.flush()

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("We are armed!")

    '''
    print("Taking off!")
    vehicle.simple_takeoff(5)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= 5 * 0.95:
            print("Reached target altitude")
            break
        time.sleep(0.25)

    '''

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
        time.sleep(backoff)
        backoff = backoff * 2


upload_mission("mission5.waypoints")

time.sleep(10)

vehicle.channels.overrides['3'] = 1500

vehicle.commands.next=0

# Set mode to AUTO to start mission
vehicle.mode = VehicleMode("AUTO")

while True:
    nextwaypoint = vehicle.commands.next
    print("Next waypoint = ", nextwaypoint)
    if nextwaypoint == len(vehicle.commands):
        break


'''
print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")
'''

while True:
    print(" Altitude: ", vehicle.location.global_relative_frame.alt)
    # Break and return from function just below target altitude.
    if vehicle.location.global_relative_frame.alt <= 0 + 1:
        print("Landed")
        break
    time.sleep(0.25)

print(math.degrees(vehicle.attitude.yaw))

connected = False

while not connected:
    ssid = wifi_module.getSSID()
    if("uniwide" in json.dumps(ssid)):
        print("We are connected!")
        connected = True
        time.sleep(5)
    else:
        print("Not connected yet...")
        time.sleep(1)


slant.runSlant()

#while not False: time.sleep(0.1)

#time.sleep(30)

try:
    input("Press enter to continue...")
    print ("")
except SyntaxError:
    pass
