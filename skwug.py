#!/usr/bin/env python3
#
#
import json
import requests


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
tempF = (tempK - 273.15) * 9/5 + 32.0
tempF = round(tempF, 2)
print("tempF=",tempF, ", type=", type(tempF))

