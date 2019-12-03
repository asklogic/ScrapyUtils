from .Command import Command
from base import core

from base.generate.generator import  create_folder, create_components
from base.exception import CmdRunException
import time
import os


class Generate(Command):
    do_collect = False
    path: str

    def syntax(self):
        return '[Generate]'

    def options(self, **kw):
        scheme = kw.get('scheme', 'Default')
        path = kw.get('path', core.PROJECT_PATH)

        # necessary property

        self.path = os.path.join(path, scheme)

    def run(self, **kw):

        path = self.path

        time.sleep(0.2)
        self.log.info('project path: ' + path)
        self.log.info('scheme name: ' + os.path.basename(path))
        time.sleep(0.2)

        if os.path.exists(path) and os.path.isdir(path):
            self.log.warning('exist path: ' + path)

        else:
            os.makedirs(path)


        # create folder
        create_folder(path)

        create_components(path)
        self.log.info('creating...')
        self._check_target()
        time.sleep(0.5)



        self.log.info('Done.')

    def exit(self):
        time.sleep(1)

    def _check_target(self):
        self.log.info('create python packages : ' + self.path)

        for file in list(os.walk(self.path))[0][2][:-1]:
            file_path = os.path.join(self.path, file)
            time.sleep(0.382)
            self.log.info('create components: ' + file_path)
            # os.remove(file_path)

        # folders (empty
        for folder in list(os.walk(self.path))[0][1]:
            time.sleep(0.382)

            folder_path = os.path.join(self.path, folder)
            self.log.info('create folder: ' + folder_path)

            # os.rmdir(folder_path)
