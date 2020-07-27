from ScrapyUtils.command.entity.check import Check
from ScrapyUtils.command.entity.generate import Generate
from ScrapyUtils.command.entity.single import Single
from ScrapyUtils.command.entity.thread_ import Thread
from ScrapyUtils.command.entity.download import Download
from ScrapyUtils.command.entity.parsing import Parsing
from ScrapyUtils.command.entity.watch import Watch

from ScrapyUtils.command.entity import Command

command_map = {
    'check': Check,
    'generate': Generate,
    'single': Single,
    'thread': Thread,
    'download': Download,
    'parsing': Parsing,
    'watch': Watch,
}


def get_command_type(command_name: str) -> Command:
    return command_map[command_name]
