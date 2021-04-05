import os
import humanize
import pygsheets as pygsheets
import datetime as dt

from .models import apiconnection
from .metrics.nsm import NorthStarMetric
from .metrics.clients import ClientsMetric


def get_eu_connection():
    api_uuid = os.environ.get('WALLARM_UUID')
    api_secret = os.environ.get('WALLARM_SECRET')
    return apiconnection.APIConnection(api='api.wallarm.com', uuid=api_uuid, secret=api_secret)


if __name__ == '__main__':
    google_client = pygsheets.authorize(service_file='credentials.json')
    spreadsheet = google_client.open('Product metrics')
    working_sheet = spreadsheet.sheet1

    EU_connection = get_eu_connection()
    metrics = [NorthStarMetric(EU_connection)]

    dates = [[2021, 1], [2021, 2], [2021, 3]]
    month_counter = 2
    for year, month in dates:
        working_sheet.cell((1, month_counter)).value = humanize.naturaldate(dt.date(year, month, 1))

        for i in range(len(metrics)):
            metric_value = metrics[i].value(year=year, month=month)
            print(metrics[i].name, 'in', year, ',', month, ' = ',
                  humanize.intword(metric_value))
            working_sheet.cell((i + 2, 1)).value = metrics[i].name
            working_sheet.cell((i + 2, month_counter)).value = metric_value

        month_counter += 1

    for i, v in enumerate(ClientsMetric.METRIC_TYPES):
        metrics = ClientsMetric(EU_connection, v)
        working_sheet.cell((10+i, 1)).value = metrics.name
        working_sheet.cell((10+i, 2)).value = metrics.value()

