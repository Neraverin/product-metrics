from wallarm_api import WallarmAPI
from weakref import WeakValueDictionary


class Singleton(type):
    _instances = WeakValueDictionary()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super(Singleton, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]


class MetricHelper(metaclass=Singleton):
    def __init__(self):
        self.real_clients = self.get_real_clients()
        self.non_superadmin_users = self.get_non_superadmin_users()

    def get_real_clients(self):
        clients = WallarmAPI().clients_api.get_clients()

        real_clients = []

        for client in clients:
            if client.is_technical == True:
                continue

            subscriptions = WallarmAPI().billing_api.get_subscription(client.id)
            if len(subscriptions) == 0:
                continue

            for subscription in subscriptions:
                if subscription.type == 'trial' or subscription.state != 'active':
                    continue

            real_clients.append(client)

        return real_clients

    def get_non_superadmin_users(self):
        non_superadmin_users = []
        for client in self.real_clients:
            users = WallarmAPI().users_api.get_users(
                {"clientid": client.id, "enabled": True})
            for user in users.users:
                if 'superadmin' and 'partner_admin' not in user.permissions:
                    non_superadmin_users.append(user.id)
        return non_superadmin_users
