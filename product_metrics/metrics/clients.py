from .base_type import BaseType
from .base_metric import BaseMetric
from .metric_helper import MetricHelper
from wallarm_api import WallarmAPI


class ClientsMetric(BaseType):
    class CountTrialClients(BaseMetric):
        def __init__(self):
            super().__init__("Trial Clients", 3)

        def value(self) -> int:
            trial_clients = 0

            for client in MetricHelper().real_clients:
                subscriptions = WallarmAPI().billing_api.get_subscription(
                    client.id)
                for subscription in subscriptions:
                    if subscription.type == 'trial' and subscription.state == 'active':
                        trial_clients += 1

            return trial_clients

    class CountPayingClients(BaseMetric):
        def __init__(self):
            super().__init__("Paying Clients", 4)

        def value(self) -> int:
            paying_clients = 0

            for client in MetricHelper().real_clients:
                subscriptions = WallarmAPI().billing_api.get_subscription(
                    client.id)
                for subscription in subscriptions:
                    if subscription.type == 'trial' or subscription.state != 'active':
                        paying_clients += 1

            return paying_clients

    class CountTechnicalClients(BaseMetric):
        def __init__(self):
            super().__init__("Technical Clients", 5)

        def value(self) -> int:
            clients = WallarmAPI().clients_api.get_clients()

            technical_clients = 0

            for client in clients:
                if client.is_technical == True:
                    technical_clients += 1

            return technical_clients

    class CountTotalClients(BaseMetric):
        def __init__(self):
            super().__init__("Total Clients", 6)

        def value(self):
            return len(WallarmAPI().clients_api.get_clients())

    def collect_metrics(self) -> list:
        return [self.CountTrialClients(),
                self.CountPayingClients(),
                self.CountTechnicalClients(),
                self.CountTotalClients()]
