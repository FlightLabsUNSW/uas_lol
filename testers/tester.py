#!/usr/bin/env python

import weather
import json

url = weather.buildUrlID(6619279)
data = weather.getWeather(url)

print json.dumps(data)

(speed, deg) = weather.getWind(data)

print speed, " ", deg

weather.checkWeather(data)