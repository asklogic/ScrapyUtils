import click
import os
import sys
import subprocess
import time

from threading import Thread

from base.command import Command, get_command_type

from base.log import set_log_file_name, set_syntax

from base.log import common as log
from base.log import basic
from base.listen import Listener, get_output, start_listener, port_connect_test


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
        with open(self.file_path) as file_:
            # Go to the end of file
            file_.seek(0, 2)
            while True:
                curr_position = file_.tell()
                line = file_.readline()
                if not line:
                    file_.seek(curr_position)
                    time.sleep(0.2)
                else:
                    print(line, end='')
                    if 'command finished.' in line:
                        break


listener = Listener()
output: None or str = None


def trigger(**kwargs):
    """
    Args:
        **kwargs:
    """
    global listener, output

    # set log
    command = get_command_type(kwargs.get('command'))

    set_syntax(command.syntax())

    if kwargs.get('background'):
        port = get_available_port()

        start_subprocess(kwargs.get('command'), kwargs.get('scheme'), port)

        output = get_subprocess_output(port)

        check_output(output)

        tail = Tail(output)

        assert start_listener(port), 'failed to start process.'

        # block
        blocking(tail.is_alive, tail.is_alive)


    else:
        # TODO: refactor
        init_output(**kwargs)

        init_listener(**kwargs)

        wait(**kwargs)

        # main command run
        if not command.command_run(**kwargs):
            log.info('failed in command_run. exiting...')
            command.failed()
            return False

        # TODO: listener paused.

        # block
        finish_case = lambda: not command.finished() and listener.finished
        blocking(finish_case, finish_case)

        command.exit()

        # if not command.config.get('keep_log') and kwargs.get('log'):
        #     pass
            # TODO: remove output
            # log.info('Deleted output. {}'.format(output))
            # if os.path.exists(output):
            #     os.remove(output)

    # FIXME: what's wrong with pyinstaller?

    sys.exit(0)


def init_output(**kwargs):
    """
    Args:
        **kwargs:
    """
    global output
    log_file_name = '-'.join((kwargs.get('command'), kwargs.get('scheme'), str(int(time.time())))[-4:]) + '.out'

    # TODO: get log file parameter
    if kwargs.get('log_file'):
        pass

    output = os.path.join(os.getcwd(), kwargs.get('scheme'), log_file_name)

    if kwargs.get('port') or kwargs.get('log'):
        basic.info('output: {}'.format(output))
        set_log_file_name(output)


def init_listener(**kwargs):
    """
    Args:
        **kwargs:
    """
    global output
    if kwargs.get('port'):
        listener.port = kwargs.get('port')
        listener.start()
        assert kwargs.get('port') == listener.port

        if output:
            listener.set_output(output)

        basic.info('listen: {}'.format(listener.port))

        sys.stdout = None


def wait(**kwargs):
    """
    Args:
        **kwargs:
    """
    if kwargs.get('confirm'):
        if listener.is_alive():
            listener.wait_to_start()
        else:
            input('press any key to continue.')


def get_available_port() -> int:
    start_port = 53000
    while port_connect_test(start_port) and start_port < 53100:
        start_port += 1

    log.info('port: {}'.format(start_port))
    return start_port


def blocking(loop_case, inner_case=None, loop_delay=0.1):
    """
    Args:
        loop_case:
        inner_case:
        loop_delay:
    """
    assert callable(loop_case), 'block case must be callable'
    assert callable(inner_case), 'block case must be callable'

    try:
        while loop_case():
            try:
                while inner_case():
                    time.sleep(loop_delay)
            except KeyboardInterrupt as e:
                print('paused.')
                pass
            # double ctrl-c delay
            time.sleep(0.618)

            # TODO: tail paused
    except KeyboardInterrupt as ke:
        # except another ctrl-c.
        print('Aborted by two ctrl-c request.')


def start_subprocess(command_name, scheme, port):
    """
    Args:
        command_name:
        scheme:
        port:
    """
    port = '--port=' + str(port)

    if getattr(sys, 'frozen', False):
        cmd_list = [sys.executable, command_name, scheme, port, '--no-background', '--log', '-c']

    else:
        executable = sys.executable
        cmd_list = [executable, 'trigger.py', command_name, scheme, port, '--no-background', '--log', '-c']

    print(cmd_list)

    p = subprocess.Popen(cmd_list,
                         shell=True,
                         # startupinfo=startupinfo,
                         creationflags=subprocess.CREATE_NO_WINDOW,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         universal_newlines=True,
                         close_fds=True,
                         # env={'PYTHONUNBUFFERED': '1'}
                         )
    return p


def get_subprocess_output(port):
    """
    Args:
        port:
    """
    output = get_output(port)
    connect_count = 0
    while connect_count < 5 and not output:
        log.debug('failed to get output from port: {}'.format(str(port)))
        connect_count += 1

        output = get_output(port)

    assert output, 'failed to get output.'
    log.info('output: {}'.format(output))

    return output


def check_output(output):
    """
    Args:
        output:
    """
    exist_count = 0
    while not os.path.exists(output) and exist_count < 6:
        time.sleep(0.5)

    assert os.path.exists(output), 'output file not exist.'
    log.debug('output file checked.')


if __name__ == '__main__':
    pass
