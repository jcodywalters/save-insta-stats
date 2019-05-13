import os
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests

# Instagram Variables
INSTAGRAM_API_ENDPOINT = 'api.instagram.com'
QUERY = 'v1/users/self/media/recent/?access_token='
USER_QUERY = 'v1/users/self/?access_token='
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

# Google API Creds
SCOPE = ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']
CREDS = ServiceAccountCredentials.from_json_keyfile_name(
    './sa-creds.json', SCOPE)
SHEET_NAME = os.getenv('SHEET_NAME')


def lambda_handler(event, context):
    main(event, context)

def get_data(host, query, access_token):
    url = f'https://{host}/{query}{access_token}'
    print('Getting follower data from {}'.format(url))
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception('ERROR - {}'.format(res.text))


def get_followers(data):
    followers = data['data']['counts']['followed_by']
    return followers


def get_google_sheet(sheet, creds):
    client = gspread.authorize(creds)
    sheet = client.open(sheet).sheet1
    return sheet


def insert_google_sheet_row(sheet, record, row):
    print('Inserting new record {} into row {}'.format(record, row))
    cell_list = sheet.range('A{}:C{}'.format(row, row))
    record.reverse()
    for cell in cell_list:
        cell.value = record.pop()
    try:
        sheet.update_cells(cell_list)
        return 'ok'
    except Exception as e:
        return 'ERROR, {}'.format(e)


def main(event=None, context=None):

    user_data = get_data(INSTAGRAM_API_ENDPOINT, USER_QUERY, ACCESS_TOKEN)
    followers = get_followers(user_data)
    print('Follower Count is {}'.format(followers))

    print('Getting Google Sheet {}'.format(SHEET_NAME))
    sheet = get_google_sheet(SHEET_NAME, CREDS)

    last_id_cell = sheet.cell(len(sheet.get_all_values()), 1)
    new_id = int(last_id_cell.value) + 1
    date = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

    new_record = [new_id, followers, date]
    row_to_insert = len(sheet.get_all_values()) + 1
    res = insert_google_sheet_row(sheet, new_record, row_to_insert)
    print(res)

if __name__ == "__main__":
    main()