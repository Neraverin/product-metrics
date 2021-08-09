from .base_type import BaseType
from .base_metric import BaseMetric
from .metric_helper import MetricHelper
from wallarm_api import WallarmAPI
from collections import Counter


class TriggersMetric(BaseType):
    def get_filters(self):
        client_filters = []
        for client in MetricHelper().real_clients:
            triggers = WallarmAPI().triggers_api.get_triggers(client.id)

            for i in triggers.triggers:
                for j in i.filters:
                    client_filters.append(j.id)

        return dict(Counter(client_filters))

    FILTER_IDS = [("Trigger by attack_type", 59, "attack_type"), 
                  ("Trigger by pool", 60,"pool"), 
                  ("Trigger by ip_address", 61,"ip_address"), 
                  ("Trigger by domain", 62,"domain"), 
                  ("Trigger by response_status", 63,"response_status"), 
                  ("Trigger by user_role", 64,"user_role"), 
                  ("Trigger by target", 65,"target"), 
                  ("Trigger by remaining_days", 66, "remaining_days"),
                  ("Trigger by url", 67, "url"), 
                  ("Trigger by hint_tag", 68, "hint_tag"), 
                  ("Trigger by subscription_type", 69, "subscription_type"), 
                  ("Trigger by threshold", 70, "threshold"), 
                  ("Trigger by max_rps", 71, "max_rps"), 
                  ("Trigger by hit_match", 72, "hit_match")]

    class CountTotalTriggers(BaseMetric):
        def __init__(self):
            super().__init__("Total triggers", 57)

        def value(self) -> int:
            total_triggers = 0
            for client in MetricHelper().real_clients:
                triggers = WallarmAPI().triggers_api.get_triggers(client.id)
                total_triggers += len(triggers.triggers)

            return total_triggers

    class CountActiveTriggers(BaseMetric):
        def __init__(self):
            super().__init__("Active triggers", 58)

        def value(self) -> int:
            active_triggers = 0
            for client in MetricHelper().real_clients:
                triggers = WallarmAPI().triggers_api.get_triggers(client.id)
                active_triggers += len([i for i in triggers.triggers if i.enabled])

            return active_triggers

    class CountFiltersByType(BaseMetric):
        def __init__(self, filters, name, row, filter_id) -> None:
            super().__init__(name, row)
            self.filter_id = filter_id
            self.filters = filters

        def value(self) -> int:
            if self.filter_id in self.filters:
                return self.filters[self.filter_id]
            else: 
                return 0

    def collect_metrics(self) -> list:
        filters = self.get_filters()
        return [self.CountTotalTriggers(),
                self.CountActiveTriggers(),
                self.CountFiltersByType(filters, *t) for t in self.FILTER_IDS]

    