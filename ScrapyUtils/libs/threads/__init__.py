from .base_thread import BaseThread
from .producer import Producer
from .consumer import Consumer

from logging import Logger

consumer_logger: Logger = None
producer_logger: Logger = None


def get_consumer_logger():
    return consumer_logger


def get_producer_looger():
    return producer_logger
