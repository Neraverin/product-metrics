import datetime as dt

from wallarm_api import WallarmAPI
from .metrics.metric_helper import MetricHelper
from .core_helper import *
from .metrics.nsm import NorthStarMetric
from .metrics.clients import ClientsMetric
from .metrics.hints import HintsMetric
from .metrics.users import UsersMetric
from .metrics.attack_rechecker import AttackRechecker
from .metrics.integrations import Integrations
from .metrics.attacks import Attacks
from .metrics.appstructure import Appstructure
from .metrics.detect_metrics.stamps import StampsMetric
from .metrics.triggers import TriggersMetric
from .metrics.node import NodeMetric
from .metrics.requests import RequestsMetric


def count_metrics(metric_types):
    current_day, _, current_month, current_year = today()
    spreadsheet = spreadsheet_connector()
    connections = get_connections()

    column = eval_column()

    for i, connection in enumerate(connections):
        api = WallarmAPI(connection.uuid, connection.secret, connection.api)

        working_sheet = spreadsheet[i]
        working_sheet.cell((1, column)).value = dt.date(
            current_year, current_month, current_day).strftime("%b %d %Y")

        for _type in metric_types:
            metrics = _type.collect_metrics()
            for metric in metrics:
                metric_name = working_sheet.cell((metric.row, 1)).value
                if metric_name != metric.name:
                    #if metric_name != '':
                     #   print("Metrics name don't match ", working_sheet, metric_name, metric.name)
                    working_sheet.cell((metric.row, 1)).value = metric.name

                working_sheet.cell((metric.row, column)
                                   ).value = metric.value()
        del api
        WallarmAPI._instances = {}
        MetricHelper._instances = {}

def requests_per_client(metric_types):
    spreadsheet = spreadsheet_connector()
    connections = get_connections()

    for i, connection in enumerate(connections):
        column = 14
        api = WallarmAPI(connection.uuid, connection.secret, connection.api)
        working_sheet = spreadsheet[11+i]

        for year in [2021]:
            for month in range(8):
                working_sheet.cell((1, column)).value = dt.date(year, month+1, 1).strftime("%b %d %Y")

                for _type in metric_types:
                    metrics = _type.collect_metrics()
                    for metric in metrics:
                        working_sheet.cell((metric.row, 1)).value = metric.name
                        working_sheet.cell((metric.row, column)
                                        ).value = metric.value(month+1, year)
                column += 1
        del api
        WallarmAPI._instances = {}
        MetricHelper._instances = {}


if __name__ == '__main__':
    types = [HintsMetric(), NorthStarMetric(), 
            ClientsMetric(), UsersMetric(), 
            AttackRechecker(), Integrations(), 
            TriggersMetric(), NodeMetric()]

    count_metrics(types)
    #requests_per_client([RequestsMetric()])
    print(f'Counted {dt.datetime.now()}')
