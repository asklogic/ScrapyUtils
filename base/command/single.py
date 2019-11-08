from typing import *
from base.command import Command

from base import core
from base.components import *
from base.libs import *
from base.command import Command

import click


@click.command()
@click.option('--count', default=1, prompt='first prompt')
def step(count):
    pass



