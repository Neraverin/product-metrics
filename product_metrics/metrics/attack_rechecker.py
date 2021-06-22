from .base_type import BaseType
from .base_metric import BaseMetric
from .metric_helper import MetricHelper

from wallarm_api import WallarmAPI


class AttackRechecker(BaseType):
    class CountAttackRecheckerModeOn(BaseMetric):
        def __init__(self):
            super().__init__("Attack Rechecker Mode On", 42)

        def value(self) -> int:
            clients_with_attack_rechecker = 0
            for client in MetricHelper().real_clients:
                if client.attack_rechecker_mode == "on":
                    print(client.id)
                    clients_with_attack_rechecker += 1

            return clients_with_attack_rechecker

    class CountVulnerabilitiesByRechecker(BaseMetric):
        def __init__(self):
            super().__init__("Vulnerabilities By Rechecker (all)", 43)

        def value(self) -> int:
            vulns_by_rechecker = 0
            i = 0

            while True:
                vulns = WallarmAPI().vulns_api.get_vulns_by_filter(
                    detection_method="attack_rechecker", limit=100, offset=i*100)
                i += 1
                vulns_by_rechecker += len(vulns)
                if len(vulns) < 100:
                    break
            return vulns_by_rechecker

    class CountVulnerabilitiesByRecheckerWithoutFalsePositives(BaseMetric):
        def __init__(self):
            super().__init__("Vulnerabilities By Rechecker (without falsepositives)", 44)

        def value(self) -> int:
            vulns_by_rechecker_without_falsepositive = 0
            i = 0

            while True:
                vulns = WallarmAPI().vulns_api.get_vulns_by_filter(
                    detection_method="attack_rechecker", limit=100, offset=i*100)
                vulns_by_rechecker_without_falsepositive += len(
                    [v for v in vulns if v.status != "falsepositive"])
                i += 1
                if len(vulns) < 100:
                    break
            return vulns_by_rechecker_without_falsepositive

    def collect_metrics(self) -> list:
        return [self.CountAttackRecheckerModeOn()]
                # self.CountVulnerabilitiesByRechecker(),
                # self.CountVulnerabilitiesByRecheckerWithoutFalsePositives()]
