#!/usr/bin/env python3
#
#
import json
import requests
from math import degrees, pi
from metpy.calc import dewpoint_from_relative_humidity
from metpy.units import units


sk_server = "10.1.1.30:3000"


# get the url for v1 API

request = "http://" + sk_server + "/signalk/"
response = requests.get(request)
endpoints = json.loads(response.text)["endpoints"]
version = endpoints["v1"]["version"]
url = endpoints["v1"]["signalk-http"]
print(version, url)

# get the weather station uuid from signalk


response = requests.get(url)
j = json.loads(response.text)
print(json.dumps(j, indent=4))
uuid = j["self"].split(".")[1]
print(uuid)

# get all the data we need

request = url + "vessels/" + uuid
print(request)
response = requests.get(request)
data = json.loads(response.text)
print(json.dumps(data, indent=4))

# process temperature

tempK = data["environment"]["outside"]["temperature"]["value"]
print("tempK=",tempK, ", type=", type(tempK))
tempC = tempK - 273.15
tempF = tempC * 9/5 + 32.0
tempF = round(tempF, 2)
print("tempF=",tempF, ", type=", type(tempF))

# process humidity

humidity = data["environment"]["outside"]["humidity"]["value"]
humidity = round(humidity * 100, 2)
print("humidity=",humidity)

# process instantaneous wind direction
winddir_rad = data["environment"]["wind"]["angleApparent"]["value"]
winddir_deg = degrees(winddir_rad)
if winddir_deg < 0.0 :
    winddir_deg += 360.0
winddir_deg = round(winddir_deg, 0)
print("winddir_deg=",winddir_deg)

# process instantaneous wind speed
windspeed_mps = data["environment"]["wind"]["speedApparent"]["value"]
windspeed_mph = windspeed_mps * 2.23694
windspeed_mph = round(windspeed_mph, 2)
print("windspeed_mph=",windspeed_mph)

# process barametric pressure
# Actual atmospheric pressure in hPa
bp_pa = data["environment"]["outside"]["pressure"]["value"]
bp_hPa = bp_pa / 100.0
# Height above sea level
hasl = 574

# Adjusted-to-the-sea barometric pressure
press_msl_hPa = bp_hPa + ((bp_hPa * 9.80665 * hasl)/(287 * (tempK + (hasl/400))))	
press_msl_in = press_msl_hPa * 0.02953
press_msl_in = round(press_msl_in, 2)
print("press_msl_in=",press_msl_in)

# process dew point
q = dewpoint_from_relative_humidity(tempC * units.degC, humidity * units.percent)
dewpoint_degC = q.m
dewpoint_degF = dewpoint_degC * 9/5 + 32 
dewpoint_degF = round(dewpoint_degF, 2)
print("dewpoint_degF=",dewpoint_degF)

# update weather underground

station_id = "ICANBE857"
password = "euFikp04"
request = "https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?ID="
request += station_id + "&PASSWORD=" + password + "&dateutc=now"
request += "&tempf=" + str(tempF) 
request += "&humidity=" + str(humidity) 
request += "&winddir=" + str(winddir_deg) 
request += "&windspeedmph=" + str(windspeed_mph) 
request += "&baromin=" + str(press_msl_in) 
request += "&dewptf=" + str(dewpoint_degF)
request += "&action=updateraw"

response = requests.get(request)
print(response)
