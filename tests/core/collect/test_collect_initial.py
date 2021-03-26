import unittest

from ScrapyUtils.core.collect import *


class TestCollectInitialTestCase(unittest.TestCase):
    def test_something(self):
        print(configure.DATA_FOLDER_PATH)
        print(configure.DOWNLOAD_FOLDER_PATH)
        print(configure.SCHEME_PATH)

        scheme_preload('atom')

        print(configure.DATA_FOLDER_PATH)
        print(configure.DOWNLOAD_FOLDER_PATH)
        print(configure.SCHEME_PATH)

        time.sleep(0.1)


        scheme_exit()


if __name__ == '__main__':
    unittest.main()
