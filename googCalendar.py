
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import time
import datetime
from datetime import timezone
from dateutil import tz
from dateutil import parser

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
    
def get_todays_agenda():
    ''' 
        Get today's agenda
    '''
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # now = (datetime.datetime.utcnow().isoformat() + 'Z')  # 'Z' indicates UTC time
    now = datetime.datetime.utcnow()
    nowMin = now.replace(hour=6).isoformat() + 'Z'
    # maxTime = (datetime.datetime.utcnow().isoformat() + 'Z')
    utcNow = datetime.datetime.utcnow()
    # This needs fixing, find 6am todays date in utc, 23:59pm in utc
    timeMax = utcNow.replace(hour=23).isoformat() + 'Z'
    print("Getting today's agenda")
    eventsResult = service.events().list(
        calendarId='primary', timeMin=nowMin, timeMax=timeMax, maxResults=7, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    responseString = "Today's Agenda: \n"

    if not events:
        responseString = 'No upcoming events found.'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        dt = parser.parse(start)
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        dt = dt.astimezone(to_zone)
        start = dt.strftime("%B %d, %Y %I:%M:%S %p")
        responseString = responseString + start + " " + event['summary'] +  " @ " + event['location'] + "\n"
        # print(start, event['summary'])
    
    return responseString


# if __name__ == '__main__':
#     main()