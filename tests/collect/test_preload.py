import unittest

from ScrapyUtils.core.preload import collect_steps, collect_processors, initial_configure


class MyTestCase(unittest.TestCase):
    def test_preload(self):
        scheme_preload('lianjia')


if __name__ == '__main__':
    unittest.main()
