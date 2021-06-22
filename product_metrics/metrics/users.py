import datetime as dt
from .base_type import BaseType
from .base_metric import BaseMetric
from .metric_helper import MetricHelper
from wallarm_api import WallarmAPI


class UsersMetric(BaseType):
    class CountActiveUsers(BaseMetric):
        def __init__(self):
            super().__init__("Active Users", 36)

        def value(self) -> int:
            active_users = 0
            for client in MetricHelper().real_clients:
                users = WallarmAPI().users_api.get_users(
                    {"clientid": client.id, "enabled": True})
                active_users += len(users.users)

            return active_users

    class CountInactiveUsers(BaseMetric):
        def __init__(self):
            super().__init__("Inactive Users", 37)

        def value(self) -> int:
            inactive_users = 0
            for client in MetricHelper().real_clients:
                users = WallarmAPI().users_api.get_users(
                    {"clientid": client.id, "enabled": False})
                inactive_users += len(users.users)

            return inactive_users

    class CountTotalUsers(BaseMetric):
        def __init__(self):
            super().__init__("Total Users", 38)

        def value(self) -> int:
            total_users = 0
            for client in MetricHelper().real_clients:
                users = WallarmAPI().users_api.get_users(
                    {"clientid": client.id})
                total_users += len(users.users)

            return total_users

    class CountLastWeekUsers(BaseMetric):
        def __init__(self):
            super().__init__("Last Week Users", 39)

        def value(self) -> int:
            last_week_users = 0
            week_delta = dt.timedelta(days=7)
            for client in MetricHelper().real_clients:
                users = WallarmAPI().users_api.get_users(
                    {"clientid": client.id, "enabled": True})
                for user in users.users:
                    if user.last_login_time:
                        delta = dt.datetime.now(
                            dt.timezone.utc) - user.last_login_time
                        if delta < week_delta:
                            last_week_users += 1

            return last_week_users

    class CountYesterdayLoginUsers(BaseMetric):
        def __init__(self):
            super().__init__("Yesterday Login Users", 35)

        def value(self) -> int:
            yesterday_users = 0
            day_delta = dt.timedelta(days=1)
            for client in MetricHelper().real_clients:
                users = WallarmAPI().users_api.get_users(
                    {"clientid": client.id, "enabled": True})
                for user in users.users:
                    if user.last_login_time:
                        delta = dt.datetime.now(
                            dt.timezone.utc) - user.last_login_time
                        if delta < day_delta:
                            yesterday_users += 1
            return yesterday_users

    class CountUsersWithoutLogin(BaseMetric):
        def __init__(self):
            super().__init__("Users Without Login", 40)

        def value(self) -> int:
            users_without_login = 0
            for client in MetricHelper().real_clients:
                users = WallarmAPI().users_api.get_users(
                    {"clientid": client.id, "enabled": True})
                for user in users.users:
                    if not user.last_login_time:
                        users_without_login += 1

            return users_without_login

    def collect_metrics(self) -> list:
        return [self.CountYesterdayLoginUsers(),
                self.CountActiveUsers(),
                self.CountInactiveUsers(),
                self.CountTotalUsers(),
                self.CountLastWeekUsers(),
                self.CountUsersWithoutLogin()]
