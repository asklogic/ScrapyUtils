from base.command.entity.check import Check
from base.command.entity.generate import Generate
from base.command.entity.single import Single
from base.command.entity.thread_ import Thread
from base.command.entity.download import Download
from base.command.entity.parsing import Parsing

from base.command.entity import Command

command_map = {
    'check': Check,
    'generate': Generate,
    'single': Single,
    'thread': Thread,
    'download': Download,
    'parsing': Parsing,
}


def get_command_type(command_name: str) -> Command:
    # TODO: exception
    """
    Args:
        command_name (str):
    """
    return command_map[command_name]
