from .base_type import BaseType
from .base_metric import BaseMetric
from product_metrics.models.apiconnection import APIConnection
from .metric_helper import real_clients_only
from wallarm_api import WallarmAPI


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
                  ("Attack rechecker (candidate)", 16, "attack_rechecker"),
                  ("Binary data (candidate)", 17, "binary_data"),
                  ("Disable attack type (candidate)", 18, "disable_attack_type"),
                  ("Parser state (candidate)", 19, "parser_state"),
                  ("Set response header (candidate)", 20, "set_response_header"),
                  ("Uploads (candidate)", 21, "uploads"),
                  ("Tag (candidate)", 22, "tag"),
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

    def __init__(self, connection: APIConnection) -> None:
        self.connection = connection
        self.api = WallarmAPI(
            connection.uuid, connection.secret, connection.api)
        self.clients = real_clients_only(self.api)

    class CountHintsByType(BaseMetric):
        def __init__(self, name, row, hint_type, clients, api) -> None:
            super().__init__(name, row)
            self.hint_type = hint_type
            self.api = api
            self.clients = clients

        def value(self):
            count_hints = 0

            for client in self.clients:
                i = 0
                while True:
                    hints = self.api.hints_api.get_hint_details(
                        type=[self.hint_type], clientid=client.id, limit=100, offset=i*100)
                    count_hints += len(hints)
                    i += 1
                    if len(hints) < 100:
                        break

            return count_hints

    class CountParserStateByParser(BaseMetric):
        def __init__(self, name, row, parser_type, clients, api) -> None:
            super().__init__(name, row)
            self.parser_type = parser_type
            self.api = api
            self.clients = clients

        def value(self):
            count_hints = 0

            for client in self.clients:
                i = 0
                while True:
                    hints = self.api.hints_api.get_hint_details(
                        type=["parser_state"], clientid=client.id, limit=100, offset=i*100)
                    for hint in hints:
                        if hint.parser == self.parser_type:
                            count_hints += 1
                    i += 1
                    if len(hints) < 100:
                        break

            return count_hints

    def collect_metrics(self):
        metrics = [self.CountHintsByType(*t, self.clients, self.api) for t in self.HINT_TYPES] + [
            self.CountParserStateByParser(*t, self.clients, self.api) for t in self.PARSER_TYPES]
        return metrics
