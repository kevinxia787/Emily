import os
import requests
import json
import geocoder

from slackclient import SlackClient
from weatherbit.api import Api
import weatherConditions as weatherConditions

degree_sign= u'\N{DEGREE SIGN}'

# Get Api Key
api_key = str(os.environ.get("WEATHERBIT_API_KEY"))

# init api
api = Api(api_key)


# Weather Advice 
listWeather = weatherConditions.get_all_weather_conditions()

# Responses
fillerOne = ["Looks like ", "Seems like ", ""]


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
  new_url = "https://api.weatherbit.io/v2.0/current?city=" + str(location.replace(" ", "")) + "&units=I&key=" + api_key
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

def check_location_exists(command, locationList):
  for location in locationList:
    if command.find(location) != -1:
      return location
    else:
      continue
  return "No locations found."

def find_key_words(keywords, command):
  for keyword in keywords:
    if command.find(keyword) != -1:
      return True
  return False

def check_severity(temp):
  if (temp < 65 and temp > 50):
    return "Bit chilly today. You should bring a jacket."
  elif (temp < 50 and temp > 35):
    return "It's pretty cold out there, bring a coat."
  elif (temp < 35):
    return "Brrr!! Layer up it's freezing out there!"
  else:
    return "It's pretty warm out there."
  

def advice_response(weather):
    if weather.find("rain") != -1 or weather.find("drizzle") != -1 and weather.find("snow") == -1:
      return "Wear a hoodie and/or bring an umbrella."
    elif weather.find("snow") != -1:
      return "Wear a thick coat and a good pair of boots."
    elif weather.find("fog") != -1:
      return "Drive safe."
    elif weather.find("Sunny") != -1 or weather.find("clear sky") != -1:
      return "Enjoy the weather!"
    elif weather.find("cloud") != -1:
      return "Hopefully it clears up!"
  


      

# print(check_location_exists("Hello I am Kevin", ["xasd", "aasd", "basd", "I am", ""]))

# print(get_weather("New York, NY"))