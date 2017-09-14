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

subprocess.check_call("getLastImageFolder3p.exe")
