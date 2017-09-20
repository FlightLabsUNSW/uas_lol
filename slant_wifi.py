import wifi_module
import json
import time


connected = False

wifi_ssid = "Verizon-MiFi7730L-2E0F"
wifi_profile = "Verizon-MiFi7730L-2E0F"


print("Connecting to verizon...")

while not connected:
    ssid = wifi_module.getSSID()
    if(wifi_ssid in json.dumps(ssid)):
        connected = wifi_module.connect(wifi_ssid, wifi_profile)
        time.sleep(5)
    else:
        print("Not connected yet...")
        time.sleep(1)

print("Verizon connected!")


try:
    input("Press enter to continue...")
    print ("")
except SyntaxError:
    pass

disconnected = False

print("Disconnecting to verizon...")

while not connected:
    ssid = wifi_module.getSSID()
    if(wifi_ssid in json.dumps(ssid)):
        connected = wifi_module.disconnect(wifi_ssid, wifi_profile)
        time.sleep(5)
    else:
        print("Not disconnected yet...")
        time.sleep(1)

print("Disconnected from verizon!")

connected = False

wifi_ssid = "0003SL3P4664"
wifi_profile = "0003SL3P4664"


print("Connecting to slant...")

while not connected:
    ssid = wifi_module.getSSID()
    if(wifi_ssid in json.dumps(ssid)):
        connected = wifi_module.connect(wifi_ssid, wifi_profile)
        time.sleep(5)
    else:
        print("Not connected yet...")
        time.sleep(1)

print("Connected to slant!")