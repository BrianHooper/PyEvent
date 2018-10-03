from datetime import datetime
import sys

from oauth2client import client
from googleapiclient import sample_tools

events_calendar_id = '8begtikb8uh1ed3s4qejnr12ss@group.calendar.google.com'

def authenticate(argv):
    # Authenticate and construct service.
    service, flags = sample_tools.init(
        argv, 'calendar', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/calendar.readonly')
    return service, flags


def get_calendars_list(service):
    calendars = []
    try:
        page_token = None
        while True:
            calendar_list = service.calendarList().list(
                pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                calendars.append(calendar_list_entry['id'])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize.')
    return calendars[1:][0]


def fetch_events(service, calendar_id=events_calendar_id):
    events_result = service.events().list(
        calendarId=calendar_id,
        singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events


def print_events(events):
    for event in events:
        summary = event['summary']
        if 'date' in event['start']:
            date = str(event['start']['date'])
            time = ""
        else:
            date = event['start']['dateTime'][:10]
            time = " @ " + event['start']['dateTime'][11:16]
        print(date + ": " + summary + time)


def main(argv):
    service, flags = authenticate(argv)
    events = fetch_events(service)
    print_events(events)


if __name__ == '__main__':
    main(sys.argv)
