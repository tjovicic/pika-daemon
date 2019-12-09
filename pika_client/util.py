import logging
import sys


def transform_payload(payload):
    payload = payload.decode('utf-8')
    return payload


def logger(name):
    root_logger = logging.getLogger(name)
    root_logger.setLevel(logging.DEBUG)
    info_handler = logging.StreamHandler(sys.stdout)
    info_handler.setLevel(logging.INFO)
    root_logger.addHandler(info_handler)

    return root_logger
