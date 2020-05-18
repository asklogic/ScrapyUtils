from base.command.entity.check import Check
from base.command.entity.generate import Generate
from base.command.entity.single import Single
from base.command.entity.thread_ import Thread
from base.command.entity.download import Download
from base.command.entity.parsing import Parsing

command_map = {
    'check': Check,
    'generate': Generate,
    'single': Single,
    'thread': Thread,
    'download': Download,
    'parsing': Parsing,
}
