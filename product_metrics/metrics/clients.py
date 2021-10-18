from .base_type import BaseType
from .base_metric import BaseMetric
from wallarm_api import WallarmAPI


class ClientsMetric(BaseType):
    def get_clients(self):
        clients = WallarmAPI().clients_api.get_clients()
        return clients

    def get_not_technical_clients(self, clients):
        not_technical_clients = [i for i in clients if i.is_technical == False]
        return not_technical_clients

    def get_active_subscriptions(self, clients):
        active_subscriptions = []
        for client in clients:
            subscriptions = WallarmAPI().billing_api.get_subscription(
                client.id)

            active_subscription = [i for i in subscriptions if i.state == 'active']
            if len(active_subscription) > 1:
                print("Client ", client.id, "have more than 1 active subscriotions ", len(active_subscriptions))
                continue

            active_subscriptions += active_subscription

        return active_subscriptions

    class CountTrialClients(BaseMetric):
        def __init__(self, active_subscriptions):
            super().__init__("Trial Clients", 3)
            self.active_subscriptions = active_subscriptions

        def value(self) -> int:
            trial_clients = [i for i in self.active_subscriptions if i.type == 'trial']
            return len(trial_clients)

    class CountPayingClients(BaseMetric):
        def __init__(self, active_subscriptions):
            super().__init__("Paying Clients", 4)
            self.active_subscriptions = active_subscriptions

        def value(self) -> int:
            paying_clients = [i for i in self.active_subscriptions if i.type != 'trial']

            return len(paying_clients)

    class CountTechnicalClients(BaseMetric):
        def __init__(self, clients):
            super().__init__("Technical Clients", 5)
            self.clients = clients

        def value(self) -> int:
            technical_clients = [i for i in self.clients if i.is_technical == True]

            return len(technical_clients)

    class CountTotalClients(BaseMetric):
        def __init__(self, clients):
            super().__init__("Total Clients", 6)
            self.clients = clients

        def value(self):
            return len(self.clients)

    def collect_metrics(self) -> list:
        clients = self.get_clients()
        not_technical_clients = self.get_not_technical_clients(clients)
        active_subscriptions = self.get_active_subscriptions(not_technical_clients)
        return [self.CountTrialClients(active_subscriptions),
                self.CountPayingClients(active_subscriptions),
                self.CountTechnicalClients(clients),
                self.CountTotalClients(clients)]
