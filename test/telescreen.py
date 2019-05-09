from watchdog.events import *
from watchdog.observers import *
import time
import os
import threading
import click

from typing import *

# path
test_path = os.path.abspath(os.path.dirname(os.getcwd()))

# args

# test_args = ['-v', '-b', '-c']
test_args = ['-v', '-c']

# init
environ = os.environ
environ["PYTHONPATH"] = test_path

import sys

sys.path.append(os.getcwd())
sys.path.append(test_path)

check_signal = False
check_count = 1
loop_signal = True

modified_info: list = []


class baseEvnetHandler(RegexMatchingEventHandler):
    # 修改次数
    check_count = 1

    def __init__(self, target: str):
        self.target = target
        re_list = [
            r".*\.py$",
        ]
        super(baseEvnetHandler, self).__init__(re_list)

    def on_modified(self, event: FileModifiedEvent):
        global check_signal
        global modified_info

        check_signal = True

        current_info = os.path.basename(event.src_path)
        if current_info not in modified_info:
            modified_info.append(current_info)


def check_thread(target: str):
    global loop_signal
    global check_signal
    global check_count
    global modified_info

    while loop_signal:

        if check_signal:
            os.system('cls')
            os.system('echo modified! {0}th changes'.format(check_count))
            os.system('echo modified info: {0}'.format('\n'.join(modified_info)))

            _single_test(target)

            check_signal = False
            check_count = check_count + 1
            modified_info.clear()

        time.sleep(1)


def _single_test(file: str):
    global test_args
    os.system('python -m unittest {0} {1}'.format(" ".join(test_args), file))


def _search_file(current_path: str) -> List[str]:
    assert os.path.exists(current_path)

    files = list(os.walk(current_path))[0][2]
    dirs = list(os.walk(current_path))[0][1]

    result = []

    result.extend([os.path.join(current_path, x) for x in files if x.endswith('.py') and not x.startswith('_')])
    for subdir in dirs:
        result.extend(_search_file(os.path.join(current_path, subdir)))
    return result


@click.group()
def cli():
    pass


@click.command()
@click.argument('folder')
@click.option('--auto', default=True, help='Auto test all file.')
def module(folder: str, auto: bool):
    target = None

    search = [os.path.join(os.getcwd(), x) for x in os.listdir(os.getcwd()) if x == folder]

    if not search:
        print('detect failed')
        return

    target = os.path.join(os.getcwd(), search[0])

    sys.path.append(target)

    for file in _search_file(target):
        os.system('cls')
        os.system('echo testing:  {}  [{}]'.format(os.path.basename(file), file))
        time.sleep(1)

        _single_test(file)
        if auto:
            time.sleep(3.5)
        else:
            input('########## enter to next ')


@click.command()
@click.argument('target')
def watch(target: str):
    if not target.endswith('.py'):
        target = target + '.py'
    target_file = None
    for file in _search_file(test_path):
        # print(os.path.basename(file))
        if os.path.basename(file) == target:
            target_file = file
            break

    if not target_file:
        print('detect file failed. Target:', target)
        return
    print('detect file. ', target_file)
    time.sleep(1)
    print("telescreen start")
    time.sleep(1)

    observer = Observer()
    event_handler = baseEvnetHandler(target)
    observer.schedule(event_handler, os.path.dirname(os.getcwd()), recursive=True)

    observer.setDaemon(True)
    observer.start()

    t = threading.Thread(target=check_thread, args=(target_file,))
    t.setDaemon(True)
    t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        loop_signal = False
        observer.stop()


cli.add_command(module)
cli.add_command(watch)

if __name__ == "__main__":
    cli()
