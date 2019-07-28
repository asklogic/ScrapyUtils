import os
from imp import reload, load_source
import sys
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler, FileModifiedEvent
import time
import threading
import linecache
from unittest import TextTestRunner, TestLoader, TestCase

pro_root = 'E:\cloudWF\RFW\ScrapyUtils'

import sys

sys.path.append('E:\cloudWF\RFW\ScrapyUtils')


class LoopTestThread(threading.Thread):

    def __init__(self, module_path, folder) -> None:
        super(LoopTestThread, self).__init__()
        self.module_path = module_path
        self.folder = folder

        self.count = 0
        self.time = time.asctime()
        self.modified_info = []

        self.stop = True
        self.changed = False
        self.target = None
        self.time_block = 1

    def run(self) -> None:

        while self.stop:
            if self.changed:
                os.system('cls')


                # TODO refact logging
                print('Telescreen activated.')
                print('[Telescreen] watch file: {0}'.format('//'.join(self.module_path)))
                print('[Telescreen] start from {}'.format(self.time))
                print('[Telescreen] changed times: {}'.format(self.count))
                print('[Telescreen] modified infos:\n* {0}'.format(
                    '\n* '.join([self.modified_info[0], self.modified_info[0]])))
                print('=' * 80)
                self.count += 1
                self.changed = False
                self.modified_info.clear()
                self._single_test()

            time.sleep(self.time_block)

    def _single_test(self):
        try:
            if not self.target:

                try:
                    self.target = __import__('.'.join(self.module_path), fromlist=[self.folder])
                    print('plan A')
                except ModuleNotFoundError as mnfe:
                    print('plan B')
                    self.target = __import__('.'.join(self.module_path[1:]), fromlist=[self.folder])
                # self.target = load_source(os.path.basename(self.module_path), self.module_path)
            reload(self.target)
        except SyntaxError as se:
            trace = se.__traceback__

            while trace.tb_next is not None:
                trace = trace.tb_next

            print('SyntaxError in  line {}: '.format(trace.tb_lineno), linecache.getline(se.filename, se.lineno),
                  end='')

            print('code:')

            [print('line [{0}]:{1}'.format(se.lineno - 3 + x, linecache.getline(se.filename, se.lineno - 3 + x)),
                   end='') for x in range(7)]
            return

        runner = TextTestRunner(verbosity=2, buffer=True)

        # TODO temp
        for d in dir(self.target):
            if d.lower() == self.module_path[-1].replace('_', '').lower():
                runner.run(TestLoader().loadTestsFromTestCase(getattr(self.target, d)))
                return

        # TODO find testcase in module
        for attr in [getattr(self.target, x) for x in dir(self.target)]:
            if issubclass(attr, TestCase):
                runner.run(TestLoader().loadTestsFromTestCase(getattr(self.target, attr.__name__)))
                return


class baseEvnetHandler(RegexMatchingEventHandler):
    # 修改次数
    check_count = 1

    def __init__(self, target: str, thread: LoopTestThread):
        self.target = target
        self.thread = thread
        re_list = [
            r".*\.py$",
        ]
        super(baseEvnetHandler, self).__init__(re_list)

    def on_modified(self, event: FileModifiedEvent):
        self.thread.changed = True
        current_info = os.path.basename(event.src_path)
        if current_info not in self.thread.modified_info:
            self.thread.modified_info.append(current_info)

        # global check_signal
        # global modified_info
        # check_signal = True\
        # current_info = os.path.basename(event.src_path)
        # if current_info not in modified_info:
        #     modified_info.append(current_info)


def watch(file_name: str, type: str = 'py', folder: str = 'tests'):
    root, file = _format(file_name, type, folder)
    path = _search_file(root, file)

    if not path:
        print('detect file failed.')
        return
    else:
        print('detect file. path:', path)

    module_path = [x.split('.')[0] for x in path.replace(pro_root, '').split('\\') if x]

    # run function in Minitrue.py

    thread = LoopTestThread(module_path, folder)
    thread.setDaemon(True)
    thread.start()

    observer = Observer()
    event_handler = baseEvnetHandler(pro_root, thread)
    observer.schedule(event_handler, os.path.dirname(pro_root), recursive=True)
    observer.setDaemon(True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('except KeyboardInterrupt')
        loop_signal = False
        observer.stop()


def _format(file_name: str, type: str = 'py', folder: str = 'tests'):
    test_root = os.path.join(pro_root, folder)

    assert os.path.exists(test_root)

    if '.' not in file_name:
        file_name = '.'.join((file_name, type))
    return test_root, file_name


def _search_file(root: str, file: str):
    files = list(os.walk(root))[0][2]
    dirs = list(os.walk(root))[0][1]

    if file in files:
        return os.path.join(root, file)
    else:
        for d in dirs:
            file_path = _search_file(os.path.join(root, d), file)
            if file_path:
                return file_path
    return False


def _observation():
    pass


if __name__ == '__main__':
    # print(_search_file(r'E:\cloudWF\RFW\ScrapyUtils', 'test_scraping.py'))
    print(sys.path)
    sys.path.remove('E:\\cloudWF\\RFW\\ScrapyUtils\\tests')
    print(sys.path)

    __import__('tests.core.test_scraping', fromlist=['core'])
    print(watch('test_scraping.py'))
