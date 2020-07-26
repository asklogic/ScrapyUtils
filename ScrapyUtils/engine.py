import logging
import os
import sys
import subprocess
import time

from ScrapyUtils.command import get_command_type

from ScrapyUtils.log import set_log_file_name, set_syntax

from ScrapyUtils.log import common as log
from ScrapyUtils.log import basic
from ScrapyUtils.listen import Listener

listener = Listener()


def trigger(**kwargs):
    options = kwargs.copy()

    command = get_command_type(options.get('command'))

    if options.get('background'):
        p = start_subprocess(kwargs.get('command'), kwargs.get('scheme'))
        options['stdout'] = p.stdout

        command = get_command_type('watch')
    else:
        listener.start()

    # update options
    command.command_collect(options)

    listener.output = init_output(options)

    # wait
    wait(options.get('confirm'))

    command.command_initial(options)

    command.start(options)

    # block
    loop_case = lambda: not command.finished()
    inner_case = lambda: not command.finished() and not listener.state

    blocking(loop_case, inner_case)

    command.exit()

    # remove log file if
    # 1. existed log file.
    # 2. command finished.
    # 3. didn't have KEEP_LOG in setting.py
    if options.get('log') and not options.get('keep_log') and command.finished():
        logging.shutdown()
        os.remove(listener.output)

    sys.exit(0)


def init_output(options):
    """initial the log's output.
    generate a output name

    Args:
        options: options dict.

    Returns: the path of the output file.

    """

    log_file_name = '-'.join((options.get('command'), options.get('scheme'), str(int(time.time())))[-4:]) + '.out'

    # TODO: get log file parameter
    if options.get('log_file'):
        pass

    output = os.path.join(os.getcwd(), options.get('scheme'), log_file_name)

    if options.get('port') or options.get('log'):
        basic.info('output: {}.'.format(output), 'Output')
        set_log_file_name(output)
        return output
    else:
        return ''


def wait(confirm: bool):
    # TODO: refactor
    if confirm:
        basic.info('===== wait to start =====')
    listener.state = confirm

    listener.block_to_start(block_state=True, timeout=-1)


def blocking(loop_case, inner_case=None, paused=lambda: True, loop_delay=0.1):
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

            # double ctrl-c delay
            time.sleep(0.618)

            if paused():
                break

    except KeyboardInterrupt as ke:
        # except another ctrl-c.
        print('Aborted by two ctrl-c request.')


def start_subprocess(command_name, scheme):
    if getattr(sys, 'frozen', False):
        cmd_list = [sys.executable, command_name, scheme, '--no-background', '--log', '-c']

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
