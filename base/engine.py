import os
import sys
import time
import threading
import socketio
from multiprocessing import Process

# import base.command.commands
# from base.log import logger
# from base import core
from threading import Thread

from base.libs import FireFoxScraper
from base.command import Command, get_command_type

from base.core import *
from base.log import set_log_file_name, set_syntax

from base.log import Wrapper as logger
from base.listen import Listener, get_output, start_listener, port_connect_test

# def single_run(target_name):
#     components = core.load_components(target_name)
#
#     prepare, schemes, models, processors = components
#
#     logger.info("single run")
#     logger.info("Target Job: " + target_name)
#     logger.info("Target Prepare: " + prepare._name + str(prepare))
#     logger.info("Target Schemes list: " + str([x._name for x in prepare.schemeList]))
#     logger.info("Target Models: " + str([x._name for x in models]))
#     logger.info("Target Process: " + str([x._name for x in processors]))
#
#     # step 3.1: build single scraper
#     scraper, tasks = core.build_prepare(prepare)
#
#     # step 3.2: build single schemes
#     schemes = core.build_schemes(schemes)
#
#     # step 3.3: build context
#     current_task = tasks[0]
#     core.load_context(current_task, schemes)
#
#     # step 3.4: build hub
#     sys_hub, dump_hub = core.build_hub(models, processors, prepare.setting)
#
#     sys_hub.scraper_activate()
#     dump_hub.scraper_activate()
#
#     # step 4: Scrapy
#     core.scrapy(schemes, scraper, current_task, dump_hub, sys_hub)
#
#     # step 5: exit
#     scraper._quit()
#     dump_hub.stop()
#     sys_hub.stop()
#
#
# def thread_run(target_name: str):
#     setting = core.build_setting(target_name)
#
#     scrapers, tasks = core.build_thread_prepare(setting.CurrentPrepare, base.command.commands.thread)
#     schemes = core.build_thread_schemes(setting.CurrentSchemeList, base.command.commands.thread)
#
#     sys_hub, dump_hub = core.build_hub(setting=setting)
#
#     logger.info("thread run")
#     logger.info("Target Job: " + target_name)
#     logger.info("Target Prepare: " + setting.CurrentPrepare._name + str(setting.CurrentPrepare))
#     logger.info("Target Schemes list: " + str([x._name for x in setting.CurrentSchemeList]))
#     logger.info("Target Models: " + str([x._name for x in setting.CurrentModels]))
#     logger.info("Target Process: " + str([x._name for x in setting.CurrentProcessorsList]))
#
#     logger.info("Detect Task number : " + str(len(tasks)))
#     logger.info("Build Scraper finish. Thread number: " + str(base.command.commands.thread))
#
#     sys_hub.scraper_activate()
#     dump_hub.scraper_activate()
#
#     for task in tasks:
#         sys_hub.save(task)
#
#     thread_List = []
#     for i in range(base.command.commands.thread):
#         t = core.ScrapyThread(sys_hub, dump_hub, schemes[i], scrapers[i], setting)
#         thread_List.append(t)
#         t.setDaemon(True)
#         t.start()
#
#     [t.join() for t in thread_List]
#     sys_hub.stop(True)
#     dump_hub.stop(True)
#
#     [x._quit() for x in scrapers]

# import logging
#
# fh = logging.FileHandler(filename='testlog.out')
# fh.setLevel(logging.DEBUG)
# fh.setFormatter(logging.Formatter(r"%(asctime)s [%(levelname)s]|%(message)s", r'%m/%d %H:%M:%S'))
#
# logger = logging.getLogger('File')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(fh)

import socket

s = socket.socket()
host = '127.0.0.1'
port = 52001

import subprocess


def port_connect(port):
    s = socket.socket()
    host = '127.0.0.1'

    try:
        s.connect((host, port))
        s.send(b'1')
        data = s.recv(1024).decode('utf-8')

        if 'scraping' in data:
            return True
        else:
            return False
    except ConnectionRefusedError as e:
        return False
    finally:
        s.close()


def stop_listener(port):
    s = socket.socket()
    host = '127.0.0.1'

    try:
        s.connect((host, port))
        s.send(b'0')

    except ConnectionRefusedError as e:
        return False
    finally:
        s.close()


def start_server():
    s = socket.socket()
    host = '127.0.0.1'
    port = 52000

    while port_connect(port) and port < 52010:
        port += 1

    s.bind((host, port))
    print('started socket server.', host, port)

    s.listen(5)

    server_flag = True

    while server_flag:
        connect, addr = s.accept()

        print('new connect!')
        logger.info('new connect!')

        try:
            command = connect.recv(1024)
            while True:

                if command == b'0':
                    break
                elif command == b'1':
                    print('test connect')
                    logger.info('test_connect')
                    connect.send(b'scraping scheme')
                else:
                    connect.send(b'no state.')

                print('loop!')
                command = connect.recv(1024)

        except Exception as e:
            print('connect closed.')
        else:
            server_flag = False
            print('connect exit.')
        finally:
            connect.close()

    print('server shutdown')
    logger.info('server shutdown')


# def tail(file) -> Thread:
#     def inner():
#         with open(file) as file_:
#             # Go to the end of file
#             file_.seek(0, 2)
#             while True:
#                 curr_position = file_.tell()
#                 line = file_.readline()
#                 if not line:
#                     file_.seek(curr_position)
#                     time.sleep(0.2)
#                 else:
#                     print(line, end='')
#
#     t = Thread(target=inner)
#     t.setDaemon(True)
#     t.start()
#     return t


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


listener = None


# temp
def listener_state():
    pass


def trigger(command_name, **kwargs):
    # set log
    command = get_command_type(command_name)

    set_syntax(command.syntax())

    # socket:
    # listener = socket_listener()

    # 1. pythonw socket command
    # 2. try to connect
    # 3. receive signal
    # 4. start socket server

    # tail the log out

    # if blocked
    # 1. run process function
    # 2. block and wait to exit

    if not kwargs.get('background'):

        port = get_available_port()
        print('starting listenner at {}'.format(port))

        background(command_name, kwargs.get('scheme'), port)

        time.sleep(1)

        # TODO: refactor output
        count = 0
        output = get_output(port)
        while count < 5 and not output:
            print('failed to get output from port: {}'.format(str(port)))
            count += 1
            output = get_output(port)
        assert output, 'failed to get output.'

        time.sleep(0.5)

        print('output:', output, )
        print('port:', port)

        tail = Tail(output)

        assert start_listener(port), 'failed to start process.'

        # block
        # main loop
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
        output = '-'.join((command.__name__, kwargs.get('scheme'), str(int(time.time())))[-4:]) + '.out'
        output = os.path.join(os.getcwd(), kwargs.get('scheme'), output)

        print('output:', output)
        set_log_file_name(output)

        if kwargs.get('port'):
            listener = Listener(kwargs.get('port'))
            assert kwargs.get('port') == listener.port

            listener.set_output(output)

            print('listen:', listener.port)

            # TODO: refactor.
            if not kwargs.get('confirm'):
                listener.wait_to_start()

            sys.stdout = None

        if not command.command_run(**kwargs):
            # TODO: failed and exit
            logger.info('failed in command_run. exiting...')
            command.failed()
            return False

        # subprocess

        # TODO: listener to global
        # blocking
        while not command.finished() and listener.block:
            time.sleep(0.2)

        command.exit()


p = None


def background(command_name, scheme, port):
    executable = r'C:\Python38\pythonw'

    port = '--port=' + str(port)
    cmd_list = [executable, command_name, scheme, port, '--background']

    if not 'python.exe' in sys.executable:
        executable = sys.executable
    else:
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


if __name__ == '__main__'
    pass
