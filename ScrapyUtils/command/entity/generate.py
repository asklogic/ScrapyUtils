from ScrapyUtils.core import core

from ScrapyUtils.generate.generator import create_folder, create_components
from ScrapyUtils.exception import CmdRunException
import time
import os

from . import Command

from ScrapyUtils.log import common as log


class Generate(Command):
    path: str

    do_collect = False

    @classmethod
    def run(cls, kwargs):
        scheme = kwargs.get('scheme', 'Default')
        relative_path = kwargs.get('path', core.PROJECT_PATH)

        # necessary property
        path = os.path.join(relative_path, scheme)
        cls.path = path

        time.sleep(0.2)
        log.info('scheme name: ' + os.path.basename(path))
        log.info('scheme absolute path: ' + path)
        time.sleep(0.2)

        if os.path.exists(path) and os.path.isdir(path):
            log.warning('exist path: ' + path)

        else:
            os.makedirs(path)

        # create folder: __init__.py and data folder.
        create_folder(path)

        # create component: py files(over write).
        create_components(path)
        log.info('creating...')
        cls._check_target()
        time.sleep(0.5)

        log.info('Done.')

    @classmethod
    def exit(cls):
        time.sleep(1)

    @classmethod
    def signal_callback(cls, signum, frame):
        """
        Args:
            signum:
            frame:
        """
        pass

    @classmethod
    def failed(cls):
        pass

    @classmethod
    def _check_target(cls):

        log.info('create python packages : ' + cls.path)

        for file in list(os.walk(cls.path))[0][2][:-1]:
            file_path = os.path.join(cls.path, file)
            time.sleep(0.382)
            log.info('create components: ' + file_path)
            # os.remove(file_path)

        # folders (empty
        for folder in list(os.walk(cls.path))[0][1]:
            time.sleep(0.382)

            folder_path = os.path.join(cls.path, folder)
            log.info('create folder: ' + folder_path)

            # os.rmdir(folder_path)
