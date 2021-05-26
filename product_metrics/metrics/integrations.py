from .base_type import BaseType
from .base_metric import BaseMetric
from .metric_helper import real_clients_only
from product_metrics.models.apiconnection import APIConnection

from wallarm_api import WallarmAPI


class Integrations(BaseType):
    INTEGRATION_TYPES = [('Slack Integration', 48, 'slack'),
                         ('Telegram Integration', 49, 'telegram'),
                         ('Email integration', 50, 'email'),
                         ('Opsgenie Integration', 51,'opsgenie'),
                         ('Pager Duty Integration', 52, 'pager_duty'),
                         ('Insight Connect Integration', 53, 'insight_connect'),
                         ('Sumo Logic Integration', 54, 'sumo_logic'),
                         ('Splunk Integration', 55, 'splunk'),]

    def __init__(self, api_connection: APIConnection) -> None:
        self.api = WallarmAPI(
            api_connection.uuid, api_connection.secret, api_connection.api)
        self.real_clients = real_clients_only(self.api)

    class CountIntegrations(BaseMetric):
        def __init__(self, api, clients):
            super().__init__("Integrations (total)", 46)
            self.api = api
            self.clients = clients

        def value(self) -> int:
            integrations = 0

            for client in self.clients:
                intgrtn = self.api.integrations_api.get_integrations(client.id)
                integrations += len(intgrtn)

            return integrations

    class CountActiveIntegrations(BaseMetric):
        def __init__(self, api, clients):
            super().__init__("Active Integrations", 47)
            self.api = api
            self.clients = clients

        def value(self) -> int:
            active_integrations = 0

            for client in self.clients:
                intgrtns = self.api.integrations_api.get_integrations(client.id)
                for intgrtn in intgrtns:
                    if intgrtn.active == True:
                        active_integrations += 1

            return active_integrations

    class CountIntegrationsByType(BaseMetric):
        def __init__(self, name, row, integration_type, clients, api):
            super().__init__(name, row)
            self.api = api
            self.clients = clients
            self.integration_type = integration_type

        def value(self) -> int:
            integrations = 0

            for client in self.clients:
                intgrtns = self.api.integrations_api.get_integrations(client.id)
                for intgrtn in intgrtns:
                    if intgrtn.type == self.integration_type:
                        integrations += 1

            return integrations

    def collect_metrics(self) -> list:
        return [self.CountIntegrationsByType(*t, self.real_clients, self.api) for t in self.INTEGRATION_TYPES] + [
            self.CountIntegrations(self.api, self.real_clients), self.CountActiveIntegrations(self.api, self.real_clients)]
