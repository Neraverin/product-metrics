import os
import datetime as dt
import pygsheets as pygsheets
from .models import apiconnection

def get_eu_connection():
    api_uuid = os.environ.get('WALLARM_UUID')
    api_secret = os.environ.get('WALLARM_SECRET')
    return apiconnection.APIConnection(api='https://api.wallarm.com', uuid=api_uuid, secret=api_secret)

def get_us_connection():
    api_uuid = os.environ.get('WALLARM_US_UUID')
    api_secret = os.environ.get('WALLARM_US_SECRET')
    return apiconnection.APIConnection(api='https://us1.api.wallarm.com', uuid=api_uuid, secret=api_secret)

def get_ru_connection():
    api_uuid = os.environ.get('WALLARM_RU_UUID')
    api_secret = os.environ.get('WALLARM_RU_SECRET')
    return apiconnection.APIConnection(api='https://api.wallarm.ru', uuid=api_uuid, secret=api_secret)

def get_connections():
    EU_connection = get_eu_connection()
    US_connection = get_us_connection()
    RU_connection = get_ru_connection()

    return [EU_connection, US_connection, RU_connection]

def today():
    now = dt.datetime.now()
    current_day = now.day
    current_month = now.month
    current_year = now.year
    current_week = now.strftime("%W")

    return current_day, int(current_week), current_month, current_year

def eval_column():
    start_year = 2021
    start_week = 26
    _, current_week, _, current_year = today()

    column = (current_week - start_week + 3) + 52 * (current_year - start_year)
    return column

def spreadsheet_connector():
    google_client = pygsheets.authorize(service_file='credentials.json')
    spreadsheet = google_client.open('Product metrics')

    return spreadsheet