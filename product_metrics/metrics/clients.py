from .base_metric import BaseMetric
from product_metrics.models.apiconnection import APIConnection

from wallarm_api import WallarmAPI



class ClientsMetric(BaseMetric):
    METRIC_TYPES = ["Trial", "Paying", "Partner", "Technical", "Total"]

    def __init__(self, api_connection: APIConnection, metric_type: METRIC_TYPES) -> None:
        self.metric_type = metric_type
        super().__init__(name=metric_type + ' Clients Metrics', connection=api_connection)

    def real_clients_only(self, api: WallarmAPI):
        clients = api.clients_api.get_clients()

        real_clients = []
        
        for client in clients:
            if client.is_technical == True:
                continue
            
            real_clients.append(client)

        return real_clients

    def partner_clients(self, api: WallarmAPI):
        clients = api.clients_api.get_clients()

        real_clients = []
        
        #for client in clients:
            #print(client.partnerid)
            
            #real_clients.append(client)

        return len(real_clients)

    def trial_clients(self, api: WallarmAPI, real_clients: list) -> int:
        trial_clients = 0

        for client in real_clients:
            subscriptions = api.billing_api.get_subscription(client.id)
            for subscription in subscriptions:
                if subscription.type == 'trial' and subscription.state == 'active':
                    trial_clients += 1

        return trial_clients

    def paying_clients(self, api: WallarmAPI, real_clients: list) -> int:
        paying_clients = 0

        for client in real_clients:
            subscriptions = api.billing_api.get_subscription(client.id)
            for subscription in subscriptions:
                if subscription.type == 'trial' or subscription.state != 'active':
                    paying_clients += 1

        return paying_clients

    def technical_clients(self, api: WallarmAPI) -> int:
        clients = api.clients_api.get_clients()

        technical_clients = 0

        for client in clients:
            if client.is_technical == True:
                technical_clients += 1

        return technical_clients

    def value(self) -> int:
        api = WallarmAPI(self.connection.uuid, self.connection.secret)
        real_clients = self.real_clients_only(api)

        if self.metric_type == "Trial":
            metric = self.trial_clients(api, real_clients)
        elif self.metric_type == "Paying":
            metric = self.paying_clients(api, real_clients)
        elif self.metric_type == "Partner":
            metric = self.partner_clients(api)
        elif self.metric_type == "Technical":
            metric = self.technical_clients(api)
        elif self.metric_type == "Total":
            metric = len(api.clients_api.get_clients())

        return metric