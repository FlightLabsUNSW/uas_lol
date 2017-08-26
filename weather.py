#!/usr/bin/env python

import sys
import json
import urllib2

DEBUG = False

api = "5c2448cb38c43a072bb865941bf0614c"

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

def checkWeather(data):
    print "Ok!"

    return True

def getWind(data):
    print data['wind']['speed'], " ", data['wind']['deg']

    return (data['wind']['speed'], data['wind']['deg'])

def buildUrlGPS(lat, lon):
    url = "http://samples.openweathermap.org/data/2.5/weather?lat=" + lat + "&lon=" + lon + "&appid=" + api
    return url

def buildUrlID(id):
    url = "http://samples.openweathermap.org/data/2.5/weather?id=" + str(id) + "&appid=" + api
    return url

def buildUrlName(name):
    url = "http://samples.openweathermap.org/data/2.5/weather?q=" + name + "&appid=" + api
    return url

def buildUrlZip(zip, countryCode):
    url = "api.openweathermap.org/data/2.5/weather?zip=" + zip + "," + countryCode + "&appid=" + api
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


