# -*- coding: utf-8 -*-
"""Example Google style docstrings.

Todo:
    * For module TODOs
    
"""
import time

from ScrapyUtils.libs.threads.base_thread import BasicThread


class MockBasic(BasicThread):

    def on_start(self):
        self.count = 0
        # input('wait for input:')


    def do_loop(self):
        print('current count:', self.count)
        self.count += 1

    def continue_loop(self) -> bool:
        return self.count > 5


if __name__ == '__main__':
    m = MockBasic(source=None)
    m.start()

    time.sleep(6)
