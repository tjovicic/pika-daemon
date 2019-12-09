from pika_client.session import Session


def create(*args, **kwargs):
    return Session(**kwargs)
