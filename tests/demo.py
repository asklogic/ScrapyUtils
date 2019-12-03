import click

import time
import threading
import random

import sys

sys.path.append(r'E:\cloudWF\RFW\ScrapyUtils')
from base.libs.thread import Consumer, ConsumerSuit


@click.group()
def cli():
    pass


@click.command()
@click.argument('target')
def thread(target: str):
    print(target)


@click.command()
@click.argument('target')
def single(target: str):
    print(target)


cli.add_command(thread)
cli.add_command(single)


def block():
    t = 5
    while t > 0:
        time.sleep(1)
        t = t - 1
        print(t)


from queue import Queue

q = Queue()
for i in range(10):
    q.put(i)







if __name__ == '__main__':
    try:
        core()
    except KeyboardInterrupt as e:
        print('exit! now!')
    except Exception as e:
        print('exit!')

