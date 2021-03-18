import os
from wallarm_api import WallarmAPI


def get_env():
    api_UUID = os.environ.get('WALLARM_UUID')
    api_secret = os.environ.get('WALLARM_SECRET')
    return api_UUID, api_secret


if __name__ == '__main__':
    api_UUID, api_secret = get_env()
    api = WallarmAPI(api_UUID, api_secret)
    client = api.clients_api.get_client()

    clients = api.clients_api.get_clients()
    for client in clients:
        subscription = api.billing_api.get_subscription(client.id)

