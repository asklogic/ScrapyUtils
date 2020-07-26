from typing import *
from threading import Thread
from time import sleep

from ScrapyUtils.log import basic
from ScrapyUtils.listen import change_state
from . import Command, ComponentMixin


class Tail(Thread):

    def __init__(self, file_path):
        """
        Args:
            file_path: log out file's absolute path
        """
        Thread.__init__(self)

        self.setDaemon(True)
        self.file_path = file_path

        self.start()

    def run(self) -> None:
        with open(self.file_path, 'r') as file_:
            # Go to the end of file
            file_.seek(0, 2)
            while True:
                curr_position = file_.tell()
                line = file_.readline()
                if not line:
                    file_.seek(curr_position)
                    sleep(0.2)
                else:
                    print(line, end='')
                    if 'command finished.' in line:
                        break


class Watch(Command):
    do_collect = False

    tail: Tail = None

    @classmethod
    def run(cls, options):
        stdout = options.get('stdout')

        lines = []
        while True:
            line = stdout.readline()
            if line == ' * ===== wait to start =====\n':
                break
            lines.append(line)

        port = lines.pop(1).split(' ')[-1].strip()[:-1]
        output = lines.pop(-1).split(' ')[-1].strip()[:-1]

        basic.info('Launched the socket succeed. Port at {}'.format(port))
        change_state(int(port))

        while True:
            line = stdout.readline()
            if line == ' * command start at 3.\n':
                break
            lines.append(line)

        lines = [x for x in lines if not x.startswith(' * <') and not x.startswith('=')]

        [print(x[:-1]) for x in lines]

        sleep(0.5)
        basic.info('-----------> Command Launched <-----------')

        cls.tail = Tail(output)

    @classmethod
    def finished(cls):
        return not cls.tail.is_alive()

    @classmethod
    def exit(cls):
        pass
