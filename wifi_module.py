import subprocess
import json

def getSSID():
    results = subprocess.check_output(["netsh", "wlan", "show", "network"])

    results = results.decode("ascii") # needed in python 3
    results = results.replace("\r","")
    ls = results.split("\n")
    ls = ls[4:]
    ssids = []
    x = 0
    while x < len(ls):
        if x % 5 == 0:
            ssids.append(ls[x])
        x += 1

    print(json.dumps(ssids))

    return ssids

def connect(ssid, profile):
    result = subprocess.check_output("netsh wlan connect ssid=" + ssid + " name=" + profile)

    if "successfully" in result:
        return True
    else:
        return False

def disconnect(ssid, profile):
    result = subprocess.check_output("netsh wlan disconnect ssid=" + ssid + " name=" + profile)

    if "successfully" in result:
        return True
    else:
        return False
