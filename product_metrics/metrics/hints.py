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
        metrics = [self.CountHintsByType("Attack rechecker rewrite (avaliable)", 3, "attack_rechecker_rewrite", self.clients, self.api),
                   self.CountHintsByType("Attack by regex (avaliable)", 4, "regex", self.clients, self.api)]

        return metrics
