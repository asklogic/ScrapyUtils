from watchdog.observers import Observer
from watchdog.events import *
import time
import os
import sys

import subprocess
import threading

path = os.path.abspath(os.path.dirname(os.getcwd()))

environ = os.environ
environ["PYTHONPATH"] = path

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
        # print(event.src_path)
        # 清屏
        # subprocess.Popen('cls', shell=True)
        #
        # subprocess.Popen(['echo', "modified! {0}th changes".format(self.check_count)], shell=True)
        # if event.is_directory:
        #     subprocess.Popen(['echo', "directory modified: {0}".format(event.src_path)], shell=True)
        # else:
        #     subprocess.Popen(['echo', "file modified: {0}".format(event.src_path)], shell=True)
        #
        #     subprocess.Popen("python -m unittest -v {0}".format(self.target), shell=True, env=environ)

        global check_signal
        global modified_info

        check_signal = True

        current_info = os.path.basename(event.src_path)
        if current_info not in modified_info:
            modified_info.append(current_info)



def check_thread():
    global loop_signal
    global check_signal
    global check_count
    global modified_info

    while loop_signal:

        if check_signal:
            # subprocess.Popen('cls', shell=True)
            # subprocess.Popen(['echo', "modified! {0}th changes".format(check_count)], shell=True)
            # subprocess.Popen("python -m unittest -v {0}".format(target), shell=True, env=environ)

            os.system('cls')
            os.system('echo modified! {0}th changes'.format(check_count))
            os.system('echo modified info: {0}'.format('\n'.join(modified_info)))

            # os.system('python -m unittest -v -c {0}'.format(target))
            os.system('python -m unittest -v -c -b {0}'.format(target))

            check_signal = False
            check_count = check_count + 1
            modified_info.clear()

        time.sleep(1)



### test
if __name__ == "__main__":
    target_name = sys.argv[1]

    target = None

    for walk in os.walk(os.getcwd()):

        if target_name in walk[2] or target_name in [x.split(".")[0] for x in walk[2]]:
            # 过滤掉 pycache
            if "__pycache__" in walk[0]:
                continue
            print(walk)

            print(os.path.join(walk[0], walk[2][[x.split(".")[0] for x in walk[2]].index(target_name)]))
            target = os.path.join(walk[0], walk[2][[x.split(".")[0] for x in walk[2]].index(target_name)])

    if not target:
        raise FileExistsError("here isn't have file name:" + target_name)

    observer = Observer()
    event_handler = baseEvnetHandler(target)
    observer.schedule(event_handler, os.path.dirname(os.getcwd()), recursive=True)
    print("telescreen start")

    observer.setDaemon(True)
    observer.start()

    t = threading.Thread(target=check_thread)
    t.setDaemon(True)

    t.start()

    # temp
    # TODO refactor daemon thread

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        loop_signal = False
        observer.stop()
