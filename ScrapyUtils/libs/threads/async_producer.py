# -*- coding: utf-8 -*-
"""Example Google style docstrings.

Todo:
    * For module TODOs
    
"""

import asyncio
import time

from abc import abstractmethod
from logging import getLogger
from typing import Any
from collections import deque

from ScrapyUtils.libs.threads.async_core import AsyncNode
from ScrapyUtils.libs.threads.async_consumer import AsyncConsumer

logger = getLogger('consumer')


class AsyncProducer(AsyncNode):

    async def do(self):

        try:
            item = await self.producing()
        except Exception as e:
            logger.error(f'failed in producing. {e}', exc_info=e)
        else:
            try:
                self.put_item(self.source, item)
            except Exception as e:
                await asyncio.sleep(0.001)
        finally:
            await asyncio.sleep(self.delay)

    @abstractmethod
    async def producing(self) -> Any:
        print('producing', time.time())
        return 'data'


if __name__ == '__main__':
    from queue import Queue

    queue = Queue()

    d = deque()

    import threading

    producer = AsyncProducer(source=d, delay=0.5)
    producer = AsyncProducer(source=d, delay=0.5)
    # producer = AsyncProducer(source=d, delay=0.2)
    # producer = AsyncProducer(source=d, delay=1)
    # producer = AsyncProducer(source=d, delay=1)

    consumer = AsyncConsumer(source=d, delay=0.1)
