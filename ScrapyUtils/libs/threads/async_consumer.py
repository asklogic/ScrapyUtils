# -*- coding: utf-8 -*-
"""Example Google style docstrings.

Todo:
    * For module TODOs
    
"""
import asyncio
import time
from abc import abstractmethod
from typing import Any
from logging import getLogger

from ScrapyUtils.libs.threads.async_core import AsyncNode

logger = getLogger('consumer')



class AsyncConsumer(AsyncNode):
    async def do(self):
        try:
            item = self.get_item(self.source)
        except Exception as e:
            await asyncio.sleep(0.001)
        else:
            try:
                await self.consuming(item)
            except Exception as e:
                logger.error(f'failed in consuming. {e}', exc_info=e)
        finally:
            # common delay
            await asyncio.sleep(self.delay)

    @abstractmethod
    async def consuming(self, item: Any):
        print('item', item, time.time())
