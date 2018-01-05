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
base_url = "https://api.weatherbit.io/v2.0/current?ip=auto&units=I&key=" + api_key
r = requests.get(base_url)
temp = ''
weather = ''
app_temp = ''
humidity = ''
weatherConditions = []





def get_weather():
  try:
    j = json.loads(r.text)
    for x in j['data']:
      temp = x['temp']
      app_temp = x['app_temp']
      weather_data = x['weather']
      humidity = x['rh']
      weather = weather_data['description']
      weatherConditions.append(temp)
      weatherConditions.append(app_temp)
      weatherConditions.append(humidity)
      weatherConditions.append(weather)
    
  except (ValueError, KeyError, TypeError):
    print("JSON format error")
  return weatherConditions


  

print(get_weather())