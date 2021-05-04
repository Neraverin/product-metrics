from .base_metric import BaseMetric
from product_metrics.models.apiconnection import APIConnection
from .helper import real_clients_only
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


class MetaHintsMetric(BaseMetric):
    def __init__(self, api_connection: APIConnection) -> None:
        super().__init__(name=' Hint Metrics',
                         connection=api_connection)

    def count(self, hint_type, clients, api):
        count_hints = 0

        for client in clients:
            i = 0
            while True:
                hints = api.hints_api.get_hint_details(
                    type=[hint_type], clientid=client.id, limit=100, offset=i*100)
                count_hints += len(hints)
                i += 1
                if len(hints) < 100:
                    break

        return hint_type, count_hints

    def value(self):
        api = WallarmAPI(self.connection.uuid,
                         self.connection.secret, self.connection.api)
        clients = real_clients_only(api)

        result_opened = {}
        result_candidates = {}
        result_internal = {}

        for hints_metric in OPENED_HINTS:
            name, value = self.count(hints_metric, clients)
            result_opened[name] = value
            print(name, value)

        for hints_metric in CANDIDATES:
            name, value = self.count(hints_metric, clients, api)
            result_candidates[name] = value
            print(name, value)

        for hints_metric in INTERNAL:
            name, value = self.count(hints_metric)
            result_internal[name] = value

        avg_opened = sum(result_opened[k] for k in result_opened)/len(clients)
        result_opened["Average opened"] = avg_opened

        avg_candidate = sum(result_candidates[k] for k in result_candidates)/len(clients)
        result_candidates["Average candidates"] = avg_candidate

        avg_internal = sum(result_internal[k] for k in result_internal)/len(clients)
        result_internal["Average internal"] = avg_internal

        return result_opened, result_candidates, result_internal

    def get_clients(self):
        api = WallarmAPI(self.connection.uuid,
                         self.connection.secret, self.connection.api)
        clients = real_clients_only(api)
        return len(clients)