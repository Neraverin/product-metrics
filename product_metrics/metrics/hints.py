from .base_type import BaseType
from .base_metric import BaseMetric
from .metric_helper import MetricHelper
from wallarm_api import WallarmAPI
from collections import Counter


class HintsMetric(BaseType):
    HINT_TYPES = [("Attack rechecker rewrite (avaliable)", 7, "attack_rechecker_rewrite"),
                  ("Attack by regex (avaliable)", 8, "regex"),
                  ("Sensitive data (avaliable)", 9, "sensitive_data"),
                  ("Vpatch (avaliable)", 10, "vpatch"),
                  ("Wallarm mode (avaliable)", 11, "wallarm_mode"),
                  ("Disable regex (avaliable)", 12, "disable_regex"),
                  ("Experimental regex (avaliable)", 13, "experimental_regex"),
                  ("Brute counter (avaliable)", 14, "brute_counter"),
                  ("Dirbust counter (avaliable)", 15, "dirbust_counter"),
                  ("Attack rechecker (avaliable)", 16, "attack_rechecker"),
                  ("Binary data (avaliable)", 17, "binary_data"),
                  ("Disable attack type (avaliable)", 18, "disable_attack_type"),
                  ("Parser state (avaliable)", 19, "parser_state"),
                  ("Set response header (avaliable)", 20, "set_response_header"),
                  ("Uploads (avaliable)", 21, "uploads"),
                  ("Tag (internal)", 22, "tag"),
                  ("Disable ld context (internal)", 23, "disable_ld_context"),
                  ("Overlimit (internal)", 24, "overlimit_res"),
                  ("Variative values (internal)", 25, "variative_values"),
                  ("Variative keys (internal)", 26, "variative_keys"),
                  ("Variative by regex (internal)", 27, "variative_by_regex"),
                  ("Max serialize data size (internal)",
                   28, "max_serialize_data_size"),
                  ("Middleware (internal)", 29, "middleware"),
                  ("Experimental stamp (internal)", 30, "experimental_stamp"),
                  ("Disable stamp (internal)", 31, "disable_stamp"),
                  ("Disable response stamp (internal)",
                   32, "disable_response_stamp"),
                  ("Experimental parser (internal)", 33, "experimental_parser"),
                  ]

    PARSER_TYPES = [("Disable parser base_64", 41, "base64")]

    HINT_TYPES_BY_USER = [("[USER] Attack rechecker rewrite", 101, "attack_rechecker_rewrite"),
                          ("[USER] Attack by regex", 102, "regex"),
                          ("[USER] Sensitive data", 103, "sensitive_data"),
                          ("[USER] Vpatch", 104, "vpatch"),
                          ("[USER] Wallarm mode", 105, "wallarm_mode"),
                          ("[USER] Disable regex", 106, "disable_regex"),
                          ("[USER] Experimental regex", 107, "experimental_regex"),
                          ("[USER] Brute counter", 108, "brute_counter"),
                          ("[USER] Dirbust counter", 109, "dirbust_counter"),
                          ("[USER] Attack rechecker", 110, "attack_rechecker"),
                          ("[USER] Binary data", 111, "binary_data"),
                          ("[USER] Disable attack type", 112, "disable_attack_type"),
                          ("[USER] Parser state", 113, "parser_state"),
                          ("[USER] Set response header", 114, "set_response_header"),
                          ("[USER] Uploads", 115, "uploads")]

    def get_hints(self):
        all_hints = []
        real_clients_id = [client.id for client in MetricHelper().real_clients]
        i = 0
        while True:
            hints = WallarmAPI().hints_api.get_hint_details(
                clientid=real_clients_id, limit=100, offset=i*100)
            all_hints += hints
            i += 1
            if len(hints) < 100:
                break

        return all_hints

    def get_hints_types(self, hints):
        types = [i.type for i in hints]
        return dict(Counter(types))

    def hints_uri_conditions(self, hints):
        uri_condition = []
        for hint in hints:
            for condition in hint.action:
                if "uri" in condition["point"]:
                    uri_condition.append(hint.id)

        return len(uri_condition)

    def get_hints_created_by_user(self):
        user_hints = []
        userids = MetricHelper().non_superadmin_users
        real_clients_id = [client.id for client in MetricHelper().real_clients]
        i = 0
        while True:
            hints = WallarmAPI().hints_api.get_hint_details(
                clientid=real_clients_id, create_userid=userids, limit=100, offset=i*100)
            user_hints += hints
            i += 1
            if len(hints) < 100:
                break

        return user_hints

    class CountHintsByType(BaseMetric):
        def __init__(self, types, name, row, hint_type) -> None:
            super().__init__(name, row)
            self.types = types
            self.hint_type = hint_type

        def value(self):
            if self.hint_type in self.types:
                return self.types[self.hint_type]
            else:
                return 0

    class CountParserStateByParser(BaseMetric):
        def __init__(self, name, row, parser_type) -> None:
            super().__init__(name, row)
            self.parser_type = parser_type

        def value(self):
            count_hints = 0

            for client in MetricHelper().real_clients:
                i = 0
                while True:
                    hints = WallarmAPI().hints_api.get_hint_details(
                        type=["parser_state"], clientid=client.id, limit=100, offset=i*100)
                    for hint in hints:
                        if hint.parser == self.parser_type:
                            count_hints += 1
                    i += 1
                    if len(hints) < 100:
                        break

            return count_hints

    class CountHintsCreatedByClient(BaseMetric):
        def __init__(self, types, name, row, hint_type) -> None:
            super().__init__(name, row)
            self.hint_type = hint_type
            self.types = types

        def value(self):
            if self.hint_type in self.types:
                return self.types[self.hint_type]
            else:
                return 0

    def collect_metrics(self):
        all_hints = self.get_hints()
        #hints_uri_condition = self.hints_uri_conditions(all_hints)
        hint_types = self.get_hints_types(all_hints)
        hints_by_user = self.get_hints_created_by_user()
        hints_by_user_types = self.get_hints_types(hints_by_user)

        metrics = [self.CountHintsCreatedByClient(hints_by_user_types, *t) for t in self.HINT_TYPES_BY_USER] + [
            self.CountHintsByType(hint_types, *t) for t in self.HINT_TYPES] + [
            self.CountParserStateByParser(*t) for t in self.PARSER_TYPES]
        return metrics
