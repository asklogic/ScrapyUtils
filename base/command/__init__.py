from .Command import get_command
from .Command import trigger
from .Command import sys_exit

from .Command import Command
from .Command import cli

from base.command import check, generate, thread, single
from base.log import Wrapper

registered = [check, generate, thread, single]

log = Wrapper
