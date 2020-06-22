import os
import sys
import subprocess
import time

from threading import Thread

from base.command import Command, get_command_type

from base.log import set_log_file_name, set_syntax

from base.log import Wrapper as logger
from base.listen import Listener, get_output, start_listener, port_connect_test


class Tail(Thread):
    def __init__(self, file_path):
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


def get_available_port() -> int:
    start_port = 53000
    while port_connect_test(start_port) and start_port < 53100:
        start_port += 1
    return start_port


listener = Listener()
output: None or str = None


def trigger(**kwargs):
    global listener, output

    # set log
    command = get_command_type(kwargs.get('command'))

    set_syntax(command.syntax())


    if kwargs.get('background'):
        port = get_available_port()

        print('starting listenner at {}'.format(port))

        start_subprocess(kwargs.get('command'), kwargs.get('scheme'), port)

        output = get_subprocess_output(port)

        time.sleep(0.5)

        print('output:', output)
        print('port:', port)

        tail = Tail(output)

        assert start_listener(port), 'failed to start process.'

        # block
        # main loop
        # TODO: common block
        try:
            while tail.is_alive():

                # inner loop
                try:
                    while tail.is_alive():
                        time.sleep(0.1)

                except KeyboardInterrupt as e:
                    # except inner ctrl-c
                    pass

                # double ctrl-c delay
                time.sleep(0.618)

                print('paused.')
                # TODO: tail paused

                print('TODO')
                # TODO: command


        except KeyboardInterrupt as ke:
            # except another ctrl-c.
            print('Aborted by two ctrl-c request.')

        # FIXME: what's wrong with pyinstaller?
        sys.exit(0)
    else:
        init_output(**kwargs)

        init_listener(**kwargs)

        wait(**kwargs)

        # main command run
        if not command.command_run(**kwargs):
            # TODO: failed and exit
            logger.info('failed in command_run. exiting...')
            command.failed()
            return False

        # TODO: listener paused.
        # blocking
        # TODO: common block
        # double loop
        while not command.finished() and listener.finished:
            time.sleep(0.2)

        command.exit()


def init_listener(**kwargs):
    global output
    if kwargs.get('port'):
        listener.port = kwargs.get('port')
        listener.start()
        assert kwargs.get('port') == listener.port

        if output:
            listener.set_output(output)

        print('listen:', listener.port)

        sys.stdout = None


def init_output(**kwargs):
    global output
    log_file_name = '-'.join((kwargs.get('command'), kwargs.get('scheme'), str(int(time.time())))[-4:]) + '.out'

    # TODO: get log file parameter
    if kwargs.get('log_file'):
        pass

    output = os.path.join(os.getcwd(), kwargs.get('scheme'), log_file_name)

    if kwargs.get('port') or kwargs.get('log'):
        print('output:', output)
        set_log_file_name(output)


def wait(**kwargs):
    if kwargs.get('confirm'):
        if listener.is_alive():
            listener.wait_to_start()
        else:
            input('press any key to continue.')


def start_subprocess(command_name, scheme, port):
    executable = r'C:\Python38\pythonw'

    port = '--port=' + str(port)
    cmd_list = [executable, command_name, scheme, port, '--no-background', '--log', '-c']

    if 'python.exe' in sys.executable:
        cmd_list.insert(1, 'trigger.py')

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
    count = 0
    output = get_output(port)
    while count < 5 and not output:
        print('failed to get output from port: {}'.format(str(port)))
        count += 1
        output = get_output(port)
    assert output, 'failed to get output.'
    return output


if __name__ == '__main__':
    pass
