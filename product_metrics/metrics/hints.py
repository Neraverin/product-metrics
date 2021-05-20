from .base_type import BaseType
from .base_metric import BaseMetric
from product_metrics.models.apiconnection import APIConnection
from .metric_helper import real_clients_only
from wallarm_api import WallarmAPI


OPENED_HINTS = ["attack_rechecker_rewrite", "regex", "sensitive_data", "vpatch",
                "wallarm_mode", "disable_regex", "experimental_regex",
                "brute_counter", "dirbust_counter"]

CANDIDATES = ['attack_rechecker', 'binary_data', 'disable_attack_type',
              'parser_state', 'parse_mode', 'parser_state', 'set_response_header', 'uploads', 'tag']

INTERNAL = ['variative_values', 'variative_keys', 'variative_by_regex',
            'max_serialize_data_size', 'middleware', 'experimental_stamp',
            'disable_stamp', 'disable_response_stamp', 'experimental_parser',
            'disable_ld_context', 'disable_base64', 'overlimit_res']


class HintsMetric(BaseType):
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

    def collect_metrics(self):
        metrics = [self.CountHintsByType("Attack rechecker rewrite (avaliable)", 7, "attack_rechecker_rewrite", self.clients, self.api),
                   self.CountHintsByType("Attack by regex (avaliable)", 8, "regex", self.clients, self.api),
                   self.CountHintsByType("Sensitive data (avaliable)", 9, "sensitive_data", self.clients, self.api),
                   self.CountHintsByType("Vpatch (avaliable)", 10, "vpatch", self.clients, self.api),
                   self.CountHintsByType("Wallarm mode (avaliable)", 11, "wallarm_mode", self.clients, self.api),
                   self.CountHintsByType("Disable regex (avaliable)", 12, "disable_regex", self.clients, self.api),
                   self.CountHintsByType("Experimental regex (avaliable)", 13, "experimental_regex", self.clients, self.api),
                   self.CountHintsByType("Brute counter (avaliable)", 14, "brute_counter", self.clients, self.api),
                   self.CountHintsByType("Dirbust counter (avaliable)", 15, "dirbust_counter", self.clients, self.api),
                   self.CountHintsByType("Attack rechecker (candidate)", 16, "attack_rechecker", self.clients, self.api),
                   self.CountHintsByType("Binary data (candidate)", 17, "binary_data", self.clients, self.api),
                   self.CountHintsByType("Disable attack type (candidate)", 18, "disable_attack_type", self.clients, self.api),
                   self.CountHintsByType("Parser state (candidate)", 19, "parser_state", self.clients, self.api),
                   self.CountHintsByType("Set response header (candidate)", 20, "set_response_header", self.clients, self.api),
                   self.CountHintsByType("Uploads (candidate)", 21, "uploads", self.clients, self.api),
                   self.CountHintsByType("Tag (candidate)", 22, "tag", self.clients, self.api),
                   self.CountHintsByType("disable_base64 (internal)", 23, "disable_base64", self.clients, self.api),
                   self.CountHintsByType("overlimit_res (internal)", 24, "overlimit_res", self.clients, self.api),
                   self.CountHintsByType("Variative values (internal)", 25, "variative_values", self.clients, self.api),
                   self.CountHintsByType("Variative keys (internal)", 26, "variative_keys", self.clients, self.api),
                   self.CountHintsByType("Variative by regex (internal)", 27, "variative_by_regex", self.clients, self.api),
                   self.CountHintsByType("Max serialize data size (internal)", 28, "max_serialize_data_size", self.clients, self.api),
                   self.CountHintsByType("Middleware (internal)", 29, "middleware", self.clients, self.api),
                   self.CountHintsByType("Experimental stamp (internal)", 30, "experimental_stamp", self.clients, self.api),
                   self.CountHintsByType("Disable stamp (internal)", 31, "disable_stamp", self.clients, self.api),
                   self.CountHintsByType("Disable response stamp (internal)", 32, "disable_response_stamp", self.clients, self.api),
                   self.CountHintsByType("Experimental parser (internal)", 33, "experimental_parser", self.clients, self.api),
                   self.CountHintsByType("Disable ld context (internal)", 34, "disable_ld_context", self.clients, self.api)
                   ]

        return metrics
