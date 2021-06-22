from .base_type import BaseType
from .base_metric import BaseMetric
from wallarm_api import WallarmAPI

SPECIAL_EU_CLIENTS = [3340, 6306, 3, 5997, 5007, 2091, 3825, 6041, 6924, 3977, 5379, 6223, 6341, 6544, 6601, 6796, 6829, 6889, 6913, 6965, 5774, 5859, 5384, 5410, 5673, 4263, 6230, 104, 156, 6923, 16, 1136, 2484, 3940, 18, 27, 6952, 4708, 390, 2421, 1648,
                   4829, 4035, 1721, 1800, 110, 742, 2090, 2280, 617, 1497, 5073, 5164, 5814, 5878, 6838, 9, 800, 1056, 5786, 6919, 3886, 106, 200, 345, 5822, 4013, 179, 1614, 23, 182, 799, 1413, 3446, 2503, 2780, 270, 1835, 1631, 2557, 4700, 6427, 4678, 6136, 2726]

start_date = int(1617224400)
end_date = int(1622322000)

interval = "01.04-30.05"

HINT_TYPES = [(f"Binary data {interval}", 64, "binary_data"),
              (f"Uploads {interval}", 65, "uploads"),
              (f"Disable attack type {interval}", 66, "disable_attack_type"),
              (f"Disable ld context (internal)", 67, "disable_ld_context"),
              (f"Disable stamp {interval}", 68, "disable_stamp"),
              (f"Parser state {interval}", 69, "parser_state"), ]

PARSER_TYPES = [(f"Disable base_64 parser {interval}", 70, "base64"),
                (f"Disable htmljs parser {interval}", 71, "htmljs")]


class Appstructure(BaseType):
    class CountFalsePositiveAttacksForSpecialClients(BaseMetric):
        def __init__(self):
            super().__init__("Falsepositive Attacks For Special Clients {interval}", 60)

        def value(self) -> int:
            fp_attacks = 0

            for clientid in SPECIAL_EU_CLIENTS:
                fp_attacks_by_client = WallarmAPI().attacks_api.get_attacks_by_filter(
                    clientid=clientid, state="falsepositive", time=[[start_date, end_date]])
                fp_attacks += len(fp_attacks_by_client)
            return fp_attacks

    class CountBASE64FalsePositiveAttacksLastMonthForSpecialClients(BaseMetric):
        def __init__(self):
            super().__init__(f"Falsepositive BASE64 Attacks For Special Clients {interval}", 61)

        def value(self) -> int:
            fp_attacks = 0

            for clientid in SPECIAL_EU_CLIENTS:
                fp_attacks_by_client = WallarmAPI().attacks_api.get_attacks_by_filter(
                    clientid=clientid, parameter="*BASE64*", state="falsepositive", time=[[start_date, end_date]])
                fp_attacks += len(fp_attacks_by_client)
            return fp_attacks

    class CountNonFalsePositiveAttacksLastMonthForSpecialClients(BaseMetric):
        def __init__(self):
            super().__init__(f"!Falsepositive Attacks For Special Clients {interval}", 62)

        def value(self) -> int:
            attacks = 0
            non_args = {"!state": "falsepositive"}

            for clientid in SPECIAL_EU_CLIENTS:
                attacks_by_client = WallarmAPI().attacks_api.get_attacks_by_filter(non_args=non_args,
                                                                                   clientid=clientid, time=[[start_date, end_date]])
                attacks += len(attacks_by_client)
            return attacks

    class CountNonFalsePositiveBASE64AttacksLastMonthForSpecialClients(BaseMetric):
        def __init__(self):
            super().__init__(f"!Falsepositive BASE64 Attacks For Special Clients {interval}", 63)

        def value(self) -> int:
            attacks = 0
            non_args = {"!state": "falsepositive"}

            for clientid in SPECIAL_EU_CLIENTS:
                attacks_by_client = WallarmAPI().attacks_api.get_attacks_by_filter(non_args=non_args,
                                                                                   clientid=clientid, parameter="*BASE64*", time=[[start_date, end_date]])
                attacks += len(attacks_by_client)
            return attacks

    class CountBASE64FalsePositiveAttacksLastMonthForSpecialClientsWithoutHTMLJS(BaseMetric):
        def __init__(self):
            super().__init__(f"Falsepositive BASE64 Attacks For Special Clients Without HTMLJS {interval}", 72)

        def value(self) -> int:
            fp_attacks = 0
            non_args = {"!parameter": "*HTMLJS*"}

            for clientid in SPECIAL_EU_CLIENTS:
                fp_attacks_by_client = WallarmAPI().attacks_api.get_attacks_by_filter(non_args=non_args,
                                                                                      clientid=clientid, parameter="*BASE64*", state="falsepositive", time=[[start_date, end_date]])
                fp_attacks += len(fp_attacks_by_client)
            return fp_attacks

    class CountHintsByType(BaseMetric):
        def __init__(self, name, row, hint_type) -> None:
            super().__init__(name, row)
            self.hint_type = hint_type

        def value(self):
            count_hints = 0

            for client in SPECIAL_EU_CLIENTS:
                i = 0
                while True:
                    hints = WallarmAPI().hints_api.get_hint_details(
                        type=[self.hint_type], clientid=client, create_time=[[start_date, end_date]], limit=100, offset=i*100)
                    count_hints += len(hints)
                    i += 1
                    if len(hints) < 100:
                        break

            return count_hints

    class CountParserStateByParser(BaseMetric):
        def __init__(self, name, row, parser_type, api) -> None:
            super().__init__(name, row)
            self.parser_type = parser_type

        def value(self):
            count_hints = 0

            for client in SPECIAL_EU_CLIENTS:
                i = 0
                while True:
                    hints = WallarmAPI().hints_api.get_hint_details(
                        type=["parser_state"], clientid=client, create_time=[[start_date, end_date]], limit=100, offset=i*100)
                    for hint in hints:
                        if hint.parser == self.parser_type:
                            count_hints += 1
                    i += 1
                    if len(hints) < 100:
                        break

            return count_hints

    def collect_metrics(self) -> list:
        return [  # self.CountFalsePositiveAttacksForSpecialClients(),
            # self.CountBASE64FalsePositiveAttacksLastMonthForSpecialClients(),
            # self.CountNonFalsePositiveAttacksLastMonthForSpecialClients(),
            # self.CountNonFalsePositiveBASE64AttacksLastMonthForSpecialClients()] + [
            # self.CountHintsByType(*t) for t in HINT_TYPES] + [
            # self.CountParserStateByParser(*t) for t in PARSER_TYPES]
            self.CountBASE64FalsePositiveAttacksLastMonthForSpecialClientsWithoutHTMLJS()]
