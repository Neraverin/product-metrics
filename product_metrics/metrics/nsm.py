from .base_type import BaseType
from .base_metric import BaseMetric
from product_metrics.models.apiconnection import APIConnection

from wallarm_api import WallarmAPI


class NorthStarMetric(BaseType):

    def __init__(self, connection: APIConnection) -> None:
        self.count_nsm = self.CountNSM(connection)

    class CountNSM(BaseMetric):
        def __init__(self, connection: APIConnection) -> None:
            super().__init__("North Star Metric", 2)
            self.connection = connection

        def value(self) -> int:
            api = WallarmAPI(self.connection.uuid, self.connection.secret)

            requests_count = 0
            clients = api.clients_api.get_clients()
            for client in clients:
                subscriptions = api.billing_api.get_subscription(client.id)
                for subscription in subscriptions:
                    if subscription.type == 'trial' or subscription.state != 'active':
                        continue

                    stats = api.graph_api.get_requests_summary_monthly(
                        client.id)
                    if stats.blocked_attacks_count > 0:
                        requests_count += stats.requests_count

                    break

            return requests_count

    def collect_metrics(self) -> list:
        return [self.count_nsm]
