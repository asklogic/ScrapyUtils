# -*- coding: utf-8 -*-
"""Example Google style docstrings.

Todo:
    * For module TODOs
    
"""
import asyncio
import threading

from abc import abstractmethod
from asyncio import gather, run
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from typing import Coroutine, List, Union, Any

from ScrapyUtils.libs.threads.source import get_bounded_method

global_thread_pool = ThreadPoolExecutor()


async def async_single_run(coroutine: Coroutine):
    await coroutine


async def async_group_run(*coroutines: List[Coroutine]):
    await gather(*coroutines)


def single_run(coroutine: Coroutine):
    global_thread_pool.submit(lambda: run(async_single_run(coroutine)))


def group_run(*coroutines: List[Coroutine]):
    global_thread_pool.submit(lambda: run(async_group_run(*coroutines)))


class AsyncNode(object):

    def __init__(self,
                 source=None,
                 start_flag: bool = True,
                 delay: Union[int, float] = 0.1,
                 event: asyncio.Event = None,
                 lock: asyncio.Lock = None,
                 ) -> None:
        self.source = source if source is not None else deque()

        get_item_method, get_size_method, put_item_method = get_bounded_method(self.source)

        self.get_item = get_item_method
        self.get_size = get_size_method
        self.put_item = put_item_method

        self.delay = delay
        self.event = event if event else asyncio.Event()
        # TODO: lock in await
        self.lock = lock if lock else asyncio.Lock()

        self.event.set()
        super().__init__()

        if start_flag:
            single_run(self.start())

    def get_size(self) -> int:
        pass

    def get_item(self) -> Any:
        pass

    def put_item(self, item: Any):
        pass

    @abstractmethod
    async def do(self):
        pass

    def pause(self):
        self.event.clear()

    def resume(self):
        self.event.set()

    async def wait(self) -> bool:
        return await self.event.wait()

    # def wait(self):
    #     return self.wait()

    async def start(self):
        while True:
            await self.wait()

            task = asyncio.create_task(self.do())
            await task
