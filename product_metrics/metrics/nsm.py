from .base_metric import BaseMetric
from product_metrics.models.apiconnection import APIConnection

from wallarm_api import WallarmAPI


class NorthStarMetric(BaseMetric):

    def __init__(self, api_connection: APIConnection) -> None:
        super().__init__(name='North Star Metric', connection=api_connection)

    def value(self, year: int, month: int) -> int:
        api = WallarmAPI(self.connection.uuid, self.connection.secret)

        requests_count = 0
        clients = api.clients_api.get_clients()
        for client in clients:
            subscriptions = api.billing_api.get_subscription(client.id)
            for subscription in subscriptions:
                if subscription.type == 'trial' or subscription.state != 'active':
                    continue

                stats = api.graph_api.get_requests_summary_monthly(client.id, year, month)
                if stats.blocked_attacks_count > 0:
                    requests_count += stats.requests_count

                break

        return requests_count
