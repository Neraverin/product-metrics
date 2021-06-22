from .base_type import BaseType
from .base_metric import BaseMetric
from wallarm_api import WallarmAPI


class NorthStarMetric(BaseType):
    class CountNSM(BaseMetric):
        def __init__(self) -> None:
            super().__init__("North Star Metric", 2)

        def value(self) -> int:
            requests_count = 0
            clients = WallarmAPI().clients_api.get_clients()
            for client in clients:
                subscriptions = WallarmAPI().billing_api.get_subscription(client.id)
                for subscription in subscriptions:
                    if subscription.type == 'trial' or subscription.state != 'active':
                        continue

                    stats = WallarmAPI().graph_api.get_requests_summary_monthly(
                        client.id)
                    if stats.blocked_attacks_count > 0:
                        requests_count += stats.requests_count

                    break

            return requests_count

    def collect_metrics(self) -> list:
        return [self.CountNSM()]
