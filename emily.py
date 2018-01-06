import os
import time
import re
from slackclient import SlackClient
import weather as weather
import parseCSV as parseCSV
import googCalendar as googCalendar


degree_sign = u'\N{DEGREE SIGN}'
locationsList = parseCSV.readCSV("uscitiesv1.3.csv")

# init Slack Client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# Emily's user ID in Slack: value is assigned after bot starts up
emily_id = None

# constants
RTM_READ_DELAY = 1 # 1 second  delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+)>(.*)"

# keywords
todaysWeather = ['today', 'now']

def parse_bot_commands(slack_events):
  '''
    Parses a list of events coming from the Slack RTM API to find bot Commands.
    If a bot command is found, this function returns a tuple of command and channel.
    If its not found, then this funtion returns None, None.
  '''
  for event in slack_events:
    if event["type"] == "message" and not "subtype" in event:
      user_id, message = parse_direct_mention(event["text"])
      if user_id == emily_id:
        return message, event["channel"]
  return None, None

def parse_direct_mention(message_text):
  '''
    Finds a direct mention (a mention that is at the beginnign) in message text
    and returns the user ID which was mentioned. if there is no direct mentioned
    returns None
  '''
  matches = re.search(MENTION_REGEX, message_text)
  # the first group contains the username, the second group contains the remaining message
  return (matches.group(1), matches.group(2).strip()) if matches else (None, None)



def handle_command(command, channel):
  '''
    Executes bot command if the command is known
  '''
  # Default response is help text for the user
  default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)
  # Location
  location = weather.check_location_exists(command, locationsList)
  # Keywords
  todaysWeatherKeyword = weather.find_key_words(todaysWeather, command)
  # Finds and executs the command, filling in response
  response = None
  # This is where you start to implement more commands!
  if "help" in command.lower():
    response = "List of known commands:" + '\n' + "Get today's weather - Type a command that contains the words 'today's weather'" + "\n" + "Today's weather in specific location - Type in a command with the words 'today's weather' and a location (City, State)" 
  elif "agenda" in command.lower():
    response = googCalendar.get_todays_agenda()
  elif "weather" and location != "No locations found.":
    weatherConditions = weather.get_weather(location)
    response = "Weather in " + location + ":" + '\n' + "Weather Conditions: " + str(weatherConditions[3]) + '\n' + "Temperature: " + str(weatherConditions[0]) + " " + degree_sign + "F" + '\n'+ "Feels like: " + str(weatherConditions[1]) + " " + degree_sign + "F" + '\n' + "Humidity: " + str(weatherConditions[2]) + "%"
  elif todaysWeatherKeyword and command.find("weather") != 1:
    weatherConditions = weather.get_weather_no_location()
    response = "Today's Weather:" + '\n' + "Weather Conditions: " + str(weatherConditions[3]) + '\n' + "Temperature: " + str(weatherConditions[0]) + " " + degree_sign + "F" + '\n'+ "Feels like: " + str(weatherConditions[1]) + " " + degree_sign + "F" + '\n' + "Humidity: " + str(weatherConditions[2]) + "%"
  elif not todaysWeatherKeyword and location == "No locations found.":
    response = "Sorry, can't find the weather for that place."
  
  # Sends the response back to the channel
  slack_client.api_call(
    "chat.postMessage",
    channel = channel,
    text=response or default_response
  )  
if __name__ == "__main__":
  if slack_client.rtm_connect(with_team_state=False):
    print("Emily connected and running!")
    # Read bot's user ID by calling Web API methhod 'auth.test'
    emily_id = slack_client.api_call("auth.test")["user_id"]
    while True:
      command, channel = parse_bot_commands(slack_client.rtm_read())
      if command:
        handle_command(command, channel)
      time.sleep(RTM_READ_DELAY)
  else:
    print("Connection failed. Exception traceblack printed above.")