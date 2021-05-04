from wallarm_api import WallarmAPI

def real_clients_only(api: WallarmAPI):
    clients = api.clients_api.get_clients()

    real_clients = []
    
    for client in clients:
        if client.is_technical == True:
            continue

        subscriptions = api.billing_api.get_subscription(client.id)
        for subscription in subscriptions:
            if subscription.type == 'trial' or subscription.state != 'active':
                continue
        
        real_clients.append(client)

    return real_clients