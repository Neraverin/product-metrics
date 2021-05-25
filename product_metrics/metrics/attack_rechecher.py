import datetime as dt
from .base_type import BaseType
from .base_metric import BaseMetric
from .metric_helper import real_clients_only
from product_metrics.models.apiconnection import APIConnection

from wallarm_api import WallarmAPI


class AttackRechecker(BaseType):
    def __init__(self, api_connection: APIConnection) -> None:
        self.api = WallarmAPI(
            api_connection.uuid, api_connection.secret, api_connection.api)
        self.real_clients = real_clients_only(self.api)

    class CountAttackRecheckerModeOn(BaseMetric):
        def __init__(self, api, clients):
            super().__init__("Attack Rechecker Mode On", 42)
            self.api = api
            self.clients = clients

        def value(self) -> int:
            clients_with_attack_rechecker = 0
            for client in self.clients:
                if client.attack_rechecker_mode == "on":
                    clients_with_attack_rechecker += 1

            return clients_with_attack_rechecker

    class CountVulnerabilitiesByRechecker(BaseMetric):
        def __init__(self, api):
            super().__init__("Vulnerabilities By Rechecker (all)", 43)
            self.api = api

        def value(self) -> int:
            vulns_by_rechecker = 0
            i = 0

            while True:
                vulns = self.api.vulns_api.get_vulns_by_filter(
                    detection_method="attack_rechecker", limit=100, offset=i*100)
                i += 1
                vulns_by_rechecker += len(vulns)
                if len(vulns) < 100:
                    break
            return vulns_by_rechecker

    class CountVulnerabilitiesByRecheckerWithountFalsePositives(BaseMetric):
        def __init__(self, api):
            super().__init__("Vulnerabilities By Rechecker (without falsepositives)", 44)
            self.api = api

        def value(self) -> int:
            vulns_by_rechecker_without_falsepositive = 0
            i = 0

            while True:
                vulns = self.api.vulns_api.get_vulns_by_filter(
                    detection_method="attack_rechecker", limit=100, offset=i*100)
                vulns_by_rechecker_without_falsepositive += len(
                    [v for v in vulns if v.status != "falsepositive"])
                i += 1
                if len(vulns) < 100:
                    break
            return vulns_by_rechecker_without_falsepositive

    def collect_metrics(self) -> list:
        return [self.CountAttackRecheckerModeOn(self.api, self.real_clients),
                self.CountVulnerabilitiesByRechecker(self.api),
                self.CountVulnerabilitiesByRecheckerWithountFalsePositives(self.api)]
