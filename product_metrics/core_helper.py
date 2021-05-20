import os
import datetime as dt
import pygsheets as pygsheets
from .models import apiconnection

def get_eu_connection():
    api_uuid = os.environ.get('WALLARM_UUID')
    api_secret = os.environ.get('WALLARM_SECRET')
    return apiconnection.APIConnection(api='https://api.wallarm.com', uuid=api_uuid, secret=api_secret)

def get_connections():
    EU_connection = get_eu_connection()

    return [EU_connection]

def today():
    now = dt.datetime.now()
    currentDay = now.day
    currentMonth = now.month
    currentYear = now.year

    return currentDay, currentMonth, currentYear

def eval_column():
    start_year = 2021
    start_month = 5
    _, currentMonth, currentYear = today()

    column = (currentMonth + 2) + 12 * (currentYear - start_year) - start_month
    return column

def spreadsheet_connector():
    google_client = pygsheets.authorize(service_file='credentials.json')
    spreadsheet = google_client.open('Product metrics')

    return spreadsheet