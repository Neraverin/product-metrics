from logging import logThreads

from pydantic.utils import truncate
from .base_type import BaseType
from .base_metric import BaseMetric
from .metric_helper import MetricHelper
from wallarm_api import WallarmAPI
from collections import Counter


class TriggersMetric(BaseType):
    FILTER_IDS = [("Trigger by attack_type", 59, "attack_type"), 
                  ("Trigger by pool", 60,"pool"), 
                  ("Trigger by ip_address", 61,"ip_address"), 
                  ("Trigger by domain", 62,"domain"), 
                  ("Trigger by response_status", 63,"response_status"), 
                  ("Trigger by user_role", 64,"user_role"), 
                  ("Trigger by target", 65,"target"), 
                  ("Trigger by url", 66, "url"), 
                  ("Trigger by hint_tag", 67, "hint_tag"), 
                  ("Trigger by threshold", 68, "threshold")]

    USER_ROLES = [("Trigger by superadmin", 69, "superadmin"),
                  ("Trigger by partner_admin", 70, "partner_admin"),
                  ("Trigger by client roles (except superadmin and partner_admin)", 71, "client")]

    def get_filters(self, all_triggers):
        client_filters = []
        for i in all_triggers:
            for j in i.filters:
                client_filters.append(j.id)

        return dict(Counter(client_filters))

    def get_triggers(self):
        all_triggers = []
        for client in MetricHelper().real_clients:
            triggers = WallarmAPI().triggers_api.get_triggers(client.id)
            all_triggers += triggers.triggers

        return all_triggers

    def get_triggers_by_creator(self):
        partner_admin_triggers = 0
        superadmin_triggers = 0
        client_triggers = 0
        for client in MetricHelper().real_clients:
            logs = WallarmAPI().audit_log_api.get_log({"action": "create", 
                                                        "object_type": "triggers.trigger", 
                                                        "subject_clientid": client.id}, limit=1000)

            for log in logs.objects:
                users = WallarmAPI().users_api.get_users({"id": log.object_userid})
                if len(users.users) == 0:
                    continue
                else:
                    user = users.users[0]

                if 'superadmin' in user.permissions:
                    superadmin_triggers += 1
                elif 'partner_admin' in user.permissions:
                    partner_admin_triggers += 1
                else:
                    client_triggers += 1

        result = {'superadmin': superadmin_triggers, 
                  'partner_admin': partner_admin_triggers, 
                  "client": client_triggers}
        return result

    class CountTotalTriggers(BaseMetric):
        def __init__(self, triggers):
            super().__init__("Total triggers", 57)
            self.triggers = triggers

        def value(self) -> int:
            return len(self.triggers)

    class CountActiveTriggers(BaseMetric):
        def __init__(self, triggers):
            super().__init__("Active triggers", 58)
            self.triggers = triggers

        def value(self) -> int:
            active_triggers = len([i for i in self.triggers if i.enabled])
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

    class CountTriggersByCreator(BaseMetric):
        def __init__(self, triggers_by_creator, name, row, role):
            super().__init__(name, row)
            self.role = role
            self.triggers_by_creator = triggers_by_creator

        def value(self) -> int:
            return self.triggers_by_creator[self.role]

    def collect_metrics(self) -> list:
        triggers = self.get_triggers()
        filters = self.get_filters(triggers)
        triggers_by_creator = self.get_triggers_by_creator()

        return [self.CountTotalTriggers(triggers), self.CountActiveTriggers(triggers)] +[
                self.CountFiltersByType(filters, *t) for t in self.FILTER_IDS] + [
                self.CountTriggersByCreator(triggers_by_creator, *t) for t in self.USER_ROLES]