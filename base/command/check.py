import time
from logging import INFO

from .Command import Command
from base import core


class Check(Command):
    require_target = True

    def syntax(self):
        return '[Check]'

    def run(self):
        setting = self.setting

        time.sleep(1)
        schemes = [str(x) for x in setting.SchemeList]

        current_schemes = [str(x) for x in setting.CurrentSchemeList]

        self.log(msg='setting schemes: \n\t' + '\n\t'.join(schemes), level=INFO)

        self.log(msg='current schemes: \n\t' + '\n\t'.join(current_schemes), level=INFO)
        time.sleep(1)

        current_models = [str(x) for x in setting.CurrentModels]

        self.log(msg='current models: \n\t' + '\n\t'.join(current_models), level=INFO)

        processors = [str(x) for x in setting.ProcessorList]
        time.sleep(1)

        current_processors = [str(x) for x in setting.CurrentProcessorsList]

        self.log(msg='setting processor: \n\t' + '\n\t'.join(processors), level=INFO)

        self.log(msg='current processor: \n\t' + '\n\t'.join(current_processors), level=INFO)
        time.sleep(1)

        start = time.time()
        scrapers, tasks = core.build_thread_prepare(setting.CurrentPrepare, setting.Thread)

        # comment this
        time.sleep(1)
        end = time.time()

        self.log('spend %.2f second(s) in' % float(end - start))


        # remain = 5
        #
        # while remain>0:
        #     remain = remain-1
        #     print('loop')
        #     time.sleep(1)