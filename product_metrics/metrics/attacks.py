import datetime as dt
from .base_type import BaseType
from .base_metric import BaseMetric
from .metric_helper import MetricHelper
from wallarm_api import WallarmAPI


class Attacks(BaseType):
    class CountFalsePositiveAttacksLastWeek(BaseMetric):
        def __init__(self):
            super().__init__("Falsepositive Attacks (last week)", 57)

        def value(self) -> int:
            week_ago_timestamp = (dt.datetime.now(
                dt.timezone.utc) - dt.timedelta(days=7)).timestamp()
            fp_attacks = 0

            for client in MetricHelper().real_clients:
                fp_attacks_by_client = WallarmAPI().attacks_api.get_attacks_by_filter(
                    clientid=client.id, state="falsepositive", time=[[int(week_ago_timestamp), None]])
                fp_attacks += len(fp_attacks_by_client)
            return fp_attacks

    class CountBase64FalsePositiveAttacksLastWeek(BaseMetric):
        def __init__(self):
            super().__init__("Falsepositive BASE64 Attacks (last week)", 58)

        def value(self) -> int:
            week_ago_timestamp = (dt.datetime.now(
                dt.timezone.utc) - dt.timedelta(days=7)).timestamp()
            fp_attacks = 0
            non_kwargs = {"!parameter": "*HTMLJS*"}

            for client in MetricHelper().real_clients:
                fp_attacks_by_client = WallarmAPI().attacks_api.get_attacks_by_filter(
                    non_kwargs=non_kwargs, parameter="*BASE64*", clientid=client.id, state="falsepositive", time=[[int(week_ago_timestamp), None]])
                fp_attacks += len(fp_attacks_by_client)
            return fp_attacks

    def collect_metrics(self) -> list:
        return [self.CountBase64FalsePositiveAttacksLastWeek()]
