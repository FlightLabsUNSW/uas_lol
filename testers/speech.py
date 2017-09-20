from __future__ import print_function
import time
import weather
import json
import math
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, mavutil
import wifi_module
import slant


import pyttsx

engine = pyttsx.init()
engine.say("Hello ................................... Connecting to vehicle... please wait...")
engine.runAndWait()