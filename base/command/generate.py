from .Command import Command
from base import core

from base.generate.generator import PROJECT_PATH, generate, create_folder, create_components
from base.exception import CmdRunException
import time
import os


class Generate(Command):

    def syntax(self):
        return '[Generate]'

    def __init__(self):
        super().__init__()

        self.target_name = ''
        self.path = ''
        self.data = True

    def signal_callback(self, signum, frame):
        # print(self, signum, frame)

        self.interrupt = True

    def options(self, **kw):
        self.target_name = kw.get('target', '')

        self.data = kw.get('data', True)

        self.path = kw.get('path', PROJECT_PATH)
        # necessary property
        assert self.path, 'no path'
        assert self.target_name, 'no target name'

    def run(self, **kw):
        path = self.path
        target_name = self.target_name

        time.sleep(0.2)
        self.log('project path: ' + path)
        self.log('target name: ' + target_name)
        time.sleep(0.2)

        # create folder
        if not create_folder(target=target_name, data=self.data):
            raise CmdRunException('Has already exist folder named: ' + target_name)

        create_components(target=target_name)
        self.log('creating...')
        time.sleep(0.5)

        self._check_target()

        self.log('Done.')

    def exit(self):
        time.sleep(1)

    def _check_target(self):
        current_path = os.path.join(PROJECT_PATH, self.target_name)
        self.log(msg='create python packages : ' + current_path)

        for file in list(os.walk(current_path))[0][2][:-1]:
            file_path = os.path.join(current_path, file)
            time.sleep(0.382)
            self.log(msg='create components: ' + file_path)
            # os.remove(file_path)

        # folders (empty
        for folder in list(os.walk(current_path))[0][1]:
            time.sleep(0.382)

            folder_path = os.path.join(current_path, folder)
            self.log(msg='create folder: ' + folder_path)

            # os.rmdir(folder_path)
