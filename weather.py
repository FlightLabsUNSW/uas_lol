#!/usr/bin/env python

import sys
import json
import urllib2

DEBUG = True

api = "5c2448cb38c43a072bb865941bf0614c"

MAX_WIND = "max_wind"
MAX_TEMP = "max_temp"
WEATHER_TYPES = "weather_types"

max_wind = 0
max_temp = 0
weather_types = []

MODE_NORMAL = 0
MODE_CHECK = 1
MODE_WIND = 2

INPUT_NONE = 0
INPUT_NAME = 1
INPUT_ID = 2
INPUT_GPS = 3
INPUT_ZIP = 4

inputs = {
    '': INPUT_NONE,
    '-n': INPUT_NAME,
    '-i': INPUT_ID,
    '-g': INPUT_GPS,
    '-z': INPUT_ZIP
}
modes = {
    '': MODE_NORMAL,
    '-n': MODE_NORMAL,
    '-x': MODE_CHECK,
    '-w': MODE_WIND
}

def getWeather(url):
    r = urllib2.urlopen(url)
    data = json.load(r)

    #print [data]
    #print "Wind speed: ", data['wind']['speed'], " Direction: ", data['wind']['deg']

    return data

def process_param(line):
    global max_wind, max_temp, weather_types
    line = line.replace(" ", "")
    s = line.split("=")
    if(len(s) < 2): return
    type = s[0]
    data = s[1]

    if type == MAX_WIND:
        max_wind = float(data)
    elif type == MAX_TEMP:
        max_temp = float(data)
    elif type == WEATHER_TYPES:
        for id in data.split(","):
            weather_types.append(int(id))

    return


def checkWeather(data):
    result = True
    #Perform checks on data here, modify result accordingly


    with open("weather_conditions.dat", "r") as f:
        for line in f:
            process_param(line)

    if DEBUG: print "Params: max_temp =", max_temp, " max_wind =", max_wind, " types =", weather_types

    temp = data["main"]["temp"]
    wind_speed = data['wind']['speed']
    type = data["weather"][0]["id"]

    if(temp > max_temp):
        result = False
    elif(wind_speed > max_wind):
        result = False
    elif not (type in weather_types):
        result = False


    print result
    return result

def getWind(data):
    print data['wind']['speed'], " ", data['wind']['deg']

    return (data['wind']['speed'], data['wind']['deg'])

def buildUrlGPS(lat, lon):
    url = "http://samples.openweathermap.org/data/2.5/weather?lat=" + str(lat) + "&lon=" + str(lon) + "&appid=" + api
    return url

def buildUrlID(id):
    url = "http://samples.openweathermap.org/data/2.5/weather?id=" + str(id) + "&appid=" + api
    return url

def buildUrlName(name):
    url = "http://samples.openweathermap.org/data/2.5/weather?q=" + name + "&appid=" + api
    return url

def buildUrlZip(zip, countryCode):
    url = "api.openweathermap.org/data/2.5/weather?zip=" + str(zip) + "," + countryCode + "&appid=" + api
    return url


if __name__ == "__main__":
    if DEBUG: print (sys.argv)

    mode = -1
    input_mode = -1

    if(len(sys.argv) <= 1):
        mode = modes['']
    else:
        if sys.argv[1] in modes:
            mode = modes[sys.argv[1]]
        else:
            sys.exit("Incorrect usage: Not a valid mode - check README")

    if(len(sys.argv) <= 2):
        input_mode = inputs['']
    else:
        if sys.argv[2] in inputs:
            input_mode = inputs[sys.argv[2]]
        else:
            sys.exit("Incorrect usage: Not a valid input mode - check READEME")




    if DEBUG: print mode
    if DEBUG: print input_mode

    url = ""

    if input_mode == INPUT_NONE:
        #No input, defaulting to Sydney weather
        url = "http://samples.openweathermap.org/data/2.5/weather?id=6619279&appid=" + api
    elif input_mode == INPUT_NAME:
        if len(sys.argv) >= 4:
            url = "http://samples.openweathermap.org/data/2.5/weather?q=" + sys.argv[3] + "&appid=" + api
            url = buildUrlName(sys.argv[3])
        else:
            sys.exit("Incorrect usage: Input expected a city name -n Sydney (check READEME)")
    elif input_mode == INPUT_ID:
        if len(sys.argv) >= 4:
            url = "http://samples.openweathermap.org/data/2.5/weather?id=" + sys.argv[3] + "&appid=" + api
            url = buildUrlID(sys.argv[3])
        else:
            sys.exit("Incorrect usage: Input expected a city id -i 6619279 (check READEME)")
    elif input_mode == INPUT_GPS:
        if len(sys.argv) >= 5:
            url = "http://samples.openweathermap.org/data/2.5/weather?lat=" + sys.argv[3] + "&lon=" + sys.argv[4] + "&appid="+ api
            url = buildUrlGPS(sys.argv[3], sys.argv[4])
        else:
            sys.exit("Incorrect usage: Input expected a city id -g <lat> <lon> (check READEME)")
    elif input_mode == INPUT_ZIP:
        if len(sys.argv) >= 5:
            url = "api.openweathermap.org/data/2.5/weather?zip=" + sys.argv[3] + "," + sys.argv[4] + "&appid=" + api
            url = buildUrlZip(sys.argv[3], sys.argv[4])
        else:
            sys.exit("Incorrect usage: Input expected a city id -i 6619279 (check READEME)")

    if DEBUG: print url
    data = getWeather(url)

    if mode == MODE_NORMAL:
        print json.dumps(data)
    elif mode == MODE_CHECK:
        checkWeather(data)
    elif mode == MODE_WIND:
        getWind(data)


