from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import json

def google_sheet_update(sheet_id, range, data):
    creds = None
    with open('driven-379206-34fddc8c7805.json', 'r') as token:
        creds = json.load(token)
        creds = Credentials.from_service_account_info(creds)

    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range).execute()
    values = result.get('values', [])

    body = {'values': data}
    value_input_option = 'RAW'

    result = service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=range,
        valueInputOption=value_input_option,
        body=body).execute()