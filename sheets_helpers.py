"""
Gets data from google sheets file ID provided in paramters.json.
"""

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from load_parameters import parameters

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SPREADSHEET_ID = parameters["spreadsheet ID"]
SPREADSHEET_NAME = parameters["spreadsheet name"]

def get_raw_data():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=SPREADSHEET_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return None
    else:
        return list(values)

def get_processed_data():
    raw_data = get_raw_data()

    DECISION_COLUMN = parameters["send email column"]
    TRIGGER = parameters["send email trigger"]
    FIRST_NAME_COLUMN = parameters["first name column"]
    EMAIL_COLUMN = parameters["email address column"]
    START_ROW = parameters["start row"]
    
    email_recipients = [
        {'first name': row[FIRST_NAME_COLUMN-1],
         'email': row[EMAIL_COLUMN-1],
        } for row in raw_data[START_ROW:] if row[DECISION_COLUMN-1] == TRIGGER]
    
    return email_recipients

if __name__ == '__main__':
    """
    For testing purposes, prints email recipients
    """
    r = get_processed_data()
    for row in r:
        print(row)
    