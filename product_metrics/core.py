import humanize
import datetime as dt

from .core_helper import *
from .metrics.nsm import NorthStarMetric
from .metrics.clients import ClientsMetric
from .metrics.hints import HintsMetric

if __name__ == '__main__':
    currentDay, currentMonth, currentYear = today()
    spreadsheet = spreadsheet_connector()
    connections = get_connections()

    column = eval_column()

    for i, connection in enumerate(connections):
        types = [NorthStarMetric(connection), HintsMetric(
            connection), ClientsMetric(connection)]

        working_sheet = spreadsheet[i]
        working_sheet.cell((1, column)).value = humanize.naturaldate(
            dt.date(currentYear, currentMonth, 1))

        for i, _type in enumerate(types):
            metrics = _type.collect_metrics()
            for metric in metrics:
                print(metric.name, metric.row, metric.value())
                working_sheet.cell((metric.row+1, 1)).value = metric.name
                working_sheet.cell((metric.row+1, column)
                                   ).value = metric.value()
