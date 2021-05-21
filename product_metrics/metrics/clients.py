from .base_type import BaseType
from .base_metric import BaseMetric
from .metric_helper import real_clients_only
from product_metrics.models.apiconnection import APIConnection

from wallarm_api import WallarmAPI


class ClientsMetric(BaseType):
    def __init__(self, api_connection: APIConnection) -> None:
        self.api = WallarmAPI(
            api_connection.uuid, api_connection.secret, api_connection.api)
        self.real_clients = real_clients_only(self.api)

        self.countTrialClients = self.CountTrialClients(
            self.api, self.real_clients)
        self.countPayingClients = self.CountPayingClients(
            self.api, self.real_clients)
        self.countTechnicalClients = self.CountTechnicalClients(self.api)
        self.countTotalClients = self.CountTotalClients(self.api)

    class CountTrialClients(BaseMetric):
        def __init__(self, api, clients):
            super().__init__("Trial Clients", 3)
            self.api = api
            self.clients = clients

        def value(self) -> int:
            trial_clients = 0

            for client in self.clients:
                subscriptions = self.api.billing_api.get_subscription(
                    client.id)
                for subscription in subscriptions:
                    if subscription.type == 'trial' and subscription.state == 'active':
                        trial_clients += 1

            return trial_clients

    class CountPayingClients(BaseMetric):
        def __init__(self, api, clients):
            super().__init__("Paying Clients", 4)
            self.api = api
            self.clients = clients

        def value(self) -> int:
            paying_clients = 0

            for client in self.clients:
                subscriptions = self.api.billing_api.get_subscription(
                    client.id)
                for subscription in subscriptions:
                    if subscription.type == 'trial' or subscription.state != 'active':
                        paying_clients += 1

            return paying_clients

    class CountTechnicalClients(BaseMetric):
        def __init__(self, api):
            super().__init__("Technical Clients", 5)
            self.api = api

        def value(self) -> int:
            clients = self.api.clients_api.get_clients()

            technical_clients = 0

            for client in clients:
                if client.is_technical == True:
                    technical_clients += 1

            return technical_clients

    class CountTotalClients(BaseMetric):
        def __init__(self, api):
            super().__init__("Total Clients", 6)
            self.api = api

        def value(self):
            return len(self.api.clients_api.get_clients())

    def collect_metrics(self) -> list:
        return [self.countTrialClients, self.countPayingClients,
                self.countTechnicalClients, self.countTotalClients]
