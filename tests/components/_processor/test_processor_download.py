import unittest
import shutil

from ScrapyUtils.command.entity.download import DownloadProcessor
from tests.components.processor.test_processor import init_processor


class DownloadProcessorCase(unittest.TestCase):

    def setUp(self) -> None:
        self.config = {
            'download_path': r'assets\download'
        }

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree('assets\download')

    def test_init(self):
        init_processor([DownloadProcessor], self.config)


if __name__ == '__main__':
    unittest.main()
