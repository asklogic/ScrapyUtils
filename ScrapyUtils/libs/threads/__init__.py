from .producer import QueueProducer, DequeProducer
from .consumer import QueueConsumer, DequeConsumer
from .base_thread import BaseThread

# Default
Consumer = QueueConsumer
Producer = QueueProducer
