import logging
import os
import sys
import subprocess
import time

from ScrapyUtils.command import get_command_type

from ScrapyUtils.log import set_log_file_name, set_syntax

from ScrapyUtils import common
from ScrapyUtils.log import common as log
from ScrapyUtils.log import basic
from ScrapyUtils.listen import Listener
# from ScrapyUtils.core import scheme_preload, scheme_initial, scheme_start, scheme_exit

listener = Listener()


def trigger(**kwargs):
    options = {'kwargs': kwargs}

    command_name = kwargs.get('command')
    scheme_name = kwargs.get('scheme')

    options['command'] = command_name
    options['scheme'] = scheme_name

    command = get_command_type(command_name)

    # TEMP
    options['exception'] = True

    # basic output
    basic.info(f'start command {command_name} process')

    # background
    if kwargs.get('background'):
        p = start_subprocess(command_name, scheme_name)
        options['stdout'] = p.stdout
        command = get_command_type('background')

    elif kwargs.get('log'):
        listener.start()
        listener.output = init_output(options)

    # wait
    wait(kwargs.get('confirm'))

    if command.do_collect:
        scheme_preload(options['kwargs'].get('scheme'))
        command.command_alter(options)
        scheme_initial(options)
        scheme_start()

    # if false: broken down in the command start, sys exit .
    # if true: continue command.
    if not command.start(options):
        sys.exit(0)

    # block
    loop_case = lambda: not command.finished()
    inner_case = lambda: not command.finished() and not listener.state

    blocking(loop_case, inner_case)

    if command.do_collect:
        scheme_exit()

    # TODO: paused and temporary exit.
    command.exit()

    # remove log file if
    # 1. existed log file.
    # 2. command finished.
    # 3. didn't have KEEP_LOG in setting.py
    if kwargs.get('log') and not kwargs.get('keep_log') and command.finished():
        logging.shutdown()
        os.remove(listener.output)

    sys.exit(0)


def init_output(options):
    """initial the log's output. generate a output name

    Returns: the path of the output file.

    Args:
        options: options dict.
    """

    kwargs = options.get('kwargs')
    command = kwargs.get('command')
    scheme = kwargs.get('scheme')

    log = kwargs.get('log')

    log_file_name = '-'.join((command, scheme, str(int(time.time())))[-4:]) + '.out'

    # TODO: get log file parameter
    # if options.get('log_file'):
    #     pass

    output = os.path.join(os.getcwd(), scheme, log_file_name)

    if log:
        basic.info('output: {}.'.format(output), 'Output')
        set_log_file_name(output)
        return output
    else:
        return ''


def wait(confirm: bool):
    # TODO: refactor
    """
    Args:
        confirm (bool):
    """
    if confirm:
        basic.info('===== wait to start =====')
    listener.state = confirm

    listener.block_to_start(block_state=True, timeout=-1)


def blocking(loop_case, inner_case=None, paused=lambda: True, loop_delay=0.1):
    """
    Args:
        loop_case:
        inner_case:
        paused:
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

            # double ctrl-c delay
            time.sleep(0.618)

            if paused():
                break

    except KeyboardInterrupt as ke:
        # except another ctrl-c.
        print('Aborted by two ctrl-c request.')


def start_subprocess(command_name, scheme):
    """
    Args:
        command_name:
        scheme:
    """
    if getattr(sys, 'frozen', False):
        cmd_list = [sys.executable, command_name, scheme, '--no-background', '--log', '--confirm']

    else:
        executable = sys.executable
        cmd_list = [executable, 'trigger.py', command_name, scheme, '--no-background', '--log', '--confirm']

    # print(cmd_list)

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


if __name__ == '__main__':
    pass
