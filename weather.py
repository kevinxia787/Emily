import os
import requests
import json
import geocoder

from slackclient import SlackClient
from weatherbit.api import Api

degree_sign= u'\N{DEGREE SIGN}'

# Get Api Key
api_key = str(os.environ.get("WEATHERBIT_API_KEY"))

# init api
api = Api(api_key)


# url


def get_weather_no_location():
  base_url = "https://api.weatherbit.io/v2.0/current?ip=auto&units=I&key=" + api_key
  r = requests.get(base_url)
  weatherConditions = []
  try:
    j = json.loads(r.text)
    for x in j['data']:
      weather_data = x['weather']
      weatherConditions.append(x['temp'])
      weatherConditions.append(x['app_temp'])
      weatherConditions.append(x['rh'])
      weatherConditions.append(weather_data['description'])
  except (ValueError, KeyError, TypeError):
    print("JSON format error")

  return weatherConditions

def get_weather(location):
  new_url = "https://api.weatherbit.io/v2.0/current?city=" + str(location) + "&units=I&key=" + api_key
  r = requests.get(new_url)
  weatherConditions = []
  try:
    j = json.loads(r.text)
    for x in j['data']:
      weather_data = x['weather']
      weatherConditions.append(x['temp'])
      weatherConditions.append(x['app_temp'])
      weatherConditions.append(x['rh'])
      weatherConditions.append(weather_data['description'])
  except  (ValueError, KeyError, TypeError):
    print("JSON format error")

  return weatherConditions

