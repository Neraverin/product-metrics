import os
import humanize

from models import apiconnection
from metrics.nsm import NorthStarMetric


def get_eu_connection():
    api_uuid = os.environ.get('WALLARM_UUID')
    api_secret = os.environ.get('WALLARM_SECRET')
    return apiconnection.APIConnection(api='api.wallarm.com', uuid=api_uuid, secret=api_secret)


if __name__ == '__main__':
    EU_connection = get_eu_connection()

    metrics = [NorthStarMetric(EU_connection)]

    dates = [[2021, 3]]
    for year, month in dates:
        for metric in metrics:
            print(metric.name, 'in', year, ',', month, ' = ', humanize.intword(metric.value(year=year, month=month)))
