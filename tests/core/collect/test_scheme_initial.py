import unittest
from typing import Optional, Any, Iterable, Mapping

from ScrapyUtils.core import *
from ScrapyUtils.core.collect import scheme_initial


class SchemeInitialTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        assert collect.step_suits == []
        assert collect.processor_suit == None

        scheme_preload('atom')

    # def test_demo(self):
    #     scheme_initial({})

    def test_default_instance(self):
        scheme_initial({})
        assert collect.step_suits != []
        assert collect.processor_suit != None

    # TODO: test output.

# def test_watcher(self):
#     from threading import Thread
#     class Watcher(Thread):
#
#         def run(self):
#             print(self.start_content, end='')
#             count = 0
#
#             char_list = ['-', '\\', '|', '/']
#             while self.exit_flag:
#                 time.sleep(self.delay)
#
#                 print('\r' + self.start_content + ' ' + char_list[count % 4], end='', flush=True)
#
#                 # if count % 5 == 3:
#                 #     print('\r' + self.start_content + ' ' + char_list[count % 4], end='', flush=True)
#                 # else:
#                 #     print('.', end='', flush=True)
#
#                 count += 1
#
#                 if count * self.delay > self.timeout:
#                     break
#             print(f'\r{self.start_content}..... {self.end_content}')
#
#         def __init__(self, timeout=20, start_content="Loading", end_content="Done!", delay=0.5,
#                      daemon=True) -> None:
#             super().__init__(daemon=daemon)
#
#             self.exit_flag = True
#             self.timeout = timeout
#             self.start_content = start_content
#             self.end_content = end_content
#             self.delay = delay
#
#             self.start()
#
#         def exit_watch(self):
#             self.exit_flag = False
#
#     w = Watcher()
#
#     time.sleep(3)
#
#     w.exit_watch()
#
#     def watch(timeout, start_content="Loading", end_content="Done!", delay=0.2):
#         print(start_content, end="")
#         for i in range(timeout):
#             print(".", end='', flush=True)
#             time.sleep(delay)
#         print(end_content)
#
#     # total = 153
#
#     # for i in range(total):
#     #     if i + 1 == total:
#     #         percent = 100.0
#     #         print('当前核算进度 : %s [%d/%d]' % (str(percent) + '%', i + 1, total), end='\n', flush=True)
#     #     else:
#     #         percent = round(1.0 * i / total * 100, 2)
#     #         print('当前核算进度 : %s [%d/%d]' % (str(percent) + '%', i + 1, total), end='\r',flush=True)
#     #     time.sleep(0.01)


if __name__ == '__main__':
    unittest.main()
