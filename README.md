# uas_lol
CREATE UAS - Repository for Land O'Lakes competition

## Windows Setup

### Prereqs

**Python**: https://www.python.org/

**MAVProxy/SITL**: http://ardupilot.org/dev/docs/sitl-native-on-windows.html#sitl-native-on-windows 

**drone-kit**: http://python.dronekit.io/contributing/developer_setup_windows.html

In CMD run the following:

```
mavproxy.exe --master=com9 --baudrate 57600 --out=udp:127.0.0.1:14550 --out=udp:127.0.0.1:14551 --console --mav10
```
See here for options on what to use as master: http://python.dronekit.io/guide/connecting_vehicle.html (Likely COM ports for Windows)

You can connect the script/Mission Planner to any of the out addresses

In a new CMD window run:
```
python test_mission.py --connect udpin:127.0.0.1:14551
```

If you are getting timeout errors check: https://github.com/dronekit/dronekit-python/blob/754ce6223dd26179045eaa394d5df0a5f787ebb2/dronekit/__init__.py#L2216

Try changing 30 --> 180

## Weather Usage

The weather script can be run as a standalone script (Will print responses to the command line) or it can be imported as a module. It uses the Open Weather Map API: https://openweathermap.org/current

Script usage is as follows:

`python weather.py -[mode] -[input_type] <input-1> <input-2>`

```
inputs = {
    '': INPUT_NONE,
    '-n': INPUT_NAME,
    '-i': INPUT_ID,
    '-g': INPUT_GPS,
    '-z': INPUT_ZIP
}
```

```
modes = {
    '': MODE_NORMAL,
    '-n': MODE_NORMAL,
    '-x': MODE_CHECK,
    '-w': MODE_WIND
}
```

### Modes

- MODE_NORMAL: Mode normal will simply print the JSON response to the screen
- MODE_CHECK: This will check whether the predefined weather conditions are satisfied
- MODE_WIND: Prints a tuple of wind data (speed, direction_in_degrees)

### Input Types

- INPUT_NONE: This will just perfom a default call to the Sydney endpoint
- INPUT_NAME: Supply the city's Name (-n Sydney)
- INPUT_ID: Supply the city's ID (-i 6619279)
- INPUT_GPS: Supply GPS Lat and Lon (-g -33.867779 151.208435)
- INPUT_ZIP: Supply the city's zip and country code (-z 94040 us)

### Weather Check Parameters
You can set the paramters for the weather check by editing the *weather_conditions.dat* file. You need to separate each parameter by a new line.

Currently supported paramters:
- **max_wind** this parameter specifies the maximum windspeed we can fly in - units in metres/sec-it takes a float input (max_wind=3.6)
- **max_temp** this paramter specifies the maximum temprature we can fly at - units in Kelvin - it takes a float input (max_temp=305.1)
- **weather_types** this parameter lists the appropriate weather types for flight - https://openweathermap.org/weather-conditions - it takes a list of integers delimited by commas (weather_types=800,801,802)

Example file:

```
max_wind=5.0
max_temp=305.1
weather_types=951,952,953,954,955,800,801,802,803,804
```
