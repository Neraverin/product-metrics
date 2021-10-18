from .base_type import BaseType
from .base_metric import BaseMetric
from .metric_helper import MetricHelper
from wallarm_api import WallarmAPI


class RequestsMetric(BaseType):
    class CountRequestsPerClient(BaseMetric):
        def __init__(self, client, row):
            super().__init__(str(client.id) + ' ' + client.name, row)
            self.client = client

        def value(self, month, year):
            requests = WallarmAPI().graph_api.get_requests_summary_monthly(client_id=self.client.id, year=year, month=month)
            return requests.requests_count

    def collect_metrics(self):
        clients = MetricHelper().real_clients
        return [self.CountRequestsPerClient(client, i+2) for i, client in enumerate(clients)]
    


