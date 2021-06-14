# -*- coding: utf-8 -*-
"""The source tool function.

Todo:
    * For module TODOs
    
"""
from asyncio import Queue as AsyncQueue
from collections import deque
from functools import partial
from queue import Queue
from typing import Any, Tuple, Union, Callable

source_list = [
    Queue,
    deque,
]


def _queue_get_item(queue: Queue, block: bool = False, timeout: float = 0.1) -> Any:
    return queue.get(block=block, timeout=timeout)


def _queue_get_size(queue: Queue) -> int:
    return queue.qsize()


def _queue_put_item(queue: Queue, item: Any, block: bool = False, timeout: float = 0.1):
    queue.put(item, block=block, timeout=timeout)


def _deque_get_item(d: deque) -> Any:
    return d.popleft()


def _deque_get_size(d: deque) -> int:
    return len(d)


def _deque_put_item(d: deque, item: Any):
    d.append(item)


def get_bounded_method(source: Union[Queue, deque]) -> Tuple[Callable, Callable, Callable]:
    """Return methods depend on the type of source."""
    current_type = type(source)
    if current_type == Queue or isinstance(source, Queue):
        return _queue_get_item, _queue_get_size, _queue_put_item
    elif current_type == deque or isinstance(source, deque):
        return _deque_get_item, _deque_get_size, _deque_put_item
    else:
        assert False, 'Source type not supported.'
