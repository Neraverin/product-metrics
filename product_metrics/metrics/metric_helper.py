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

    def get_real_clients(self):
        clients = WallarmAPI().clients_api.get_clients()

        real_clients = []

        for client in clients:
            if client.is_technical == True:
                continue

            subscriptions = WallarmAPI().billing_api.get_subscription(client.id)
            for subscription in subscriptions:
                if subscription.type == 'trial' or subscription.state != 'active':
                    continue

            real_clients.append(client)

        return real_clients
