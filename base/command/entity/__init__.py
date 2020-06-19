from abc import abstractmethod
from queue import Queue
from typing import List, Callable

from base.components import StepSuit, Pipeline, log
from base.libs import Producer
from base.core import *


class Command(object):
    exitcode: int = 0
    interrupt: bool = False

    do_collect: bool = True

    # def __init__(self):
    #     self.exitcode: int = 0
    #     self.interrupt: bool = False
    #     self.do_collect = True

    @classmethod
    def syntax(cls):
        return '[Command]'

    @classmethod
    def command_config(cls, **kwargs):
        """
        alter command.config
        """
        pass

    @classmethod
    def command_components(cls, steps, processors, **kwargs):
        """
        alter command's components
        """
        return steps, processors

    @classmethod
    def command_scraper(cls, **kwargs) -> None or Callable:
        """
        alter command.scraper
        """
        return None

    @classmethod
    def command_task(cls, **kwargs) -> None or Callable:
        """
        alter command.tasks
        """
        return None

    @classmethod
    def command_logout(cls):
        log.info('########### suit components ##########', 'System')
        log.info('### ' + ' - '.join([x.name for x in get_steps()]), 'System')
        log.info('######## processor components ########', 'System')
        log.info('### ' + ' - '.join([x.name for x in get_processors()]), 'System')
        log.info('######################################', 'System')

    @classmethod
    def command_collect(cls, **kwargs):
        log.info('collect command {}'.format(cls.__name__), 'collect')

        if not cls.do_collect:
            return
        try:
            collect_scheme_preload(kwargs.get('scheme'))

            # config
            cls.config = get_config()
            cls.command_config(**kwargs)

            # alter components
            steps, processors = cls.command_components(get_steps(), get_processors(), **kwargs)
            set_steps(steps)
            set_processors(processors)

            # alter scraper
            scraper = cls.command_scraper(**kwargs)
            if scraper:
                set_scraper_callable(scraper)

            # alter task
            task = cls.command_task(**kwargs)
            if task:
                set_task_callable(task)

            cls.command_logout()

        except AssertionError as ae:
            # TODO: assert error
            log.error("assert error in collecting of command '{}'. ".format(cls.__name__), 'collect')
            log.exception('Command', ae, 0)

        except Exception as e:
            log.error("some error in collecting of command '{}'. ".format(cls.__name__), 'collect')
            log.exception('Command', e, 0)
        else:
            return True

    @classmethod
    def command_initial(cls, **kwargs):
        try:
            # initial scheme
            collect_scheme_initial(**kwargs)
        except AssertionError as ae:
            # TODO: assert error
            log.error("assert error in initializing of command '{}'. ".format(cls.__name__), 'initial')
            log.exception('Command', ae, 0)

        except Exception as e:
            log.error("some error in initializing of command '{}'. ".format(cls.__name__), 'initial')
            log.exception('Command', e, 0)
        else:
            cls.suits = get_suits()
            cls.tasks = get_tasks()
            cls.pipeline = get_pipeline()
            cls.proxy = get_proxy()

            # TODO: proxy start.
            if cls.proxy:
                cls.proxy.start()
            return True

    @classmethod
    def command_process(cls, **kwargs):
        log.info('processing command {}'.format(cls.__name__), 'System')
        try:

            log.debug('command running...', 'Processing')

            cls.run(kwargs)

        except AssertionError as ae:
            # TODO: assert error
            log.error("assert error in processing of command '{}'. ".format(cls.__name__), 'process')
            log.exception('Command', ae, 0)

        except Exception as e:
            log.error("some error in processing of command '{}'. ".format(cls.__name__), 'process')
            log.exception('Command', e)
        else:
            return True

    @classmethod
    def command_run(cls, **kwargs):
        # TODO: need refactor.
        if not cls.command_collect(**kwargs):
            return False

        if not cls.command_initial(**kwargs):
            return False

        if not cls.command_process(**kwargs):
            return False

        return True

    @classmethod
    @abstractmethod
    def run(cls, kw):
        pass

    @classmethod
    @abstractmethod
    def finished(cls):
        return True

    @classmethod
    @abstractmethod
    def failed(cls):
        pass

    @classmethod
    @abstractmethod
    def signal_callback(cls, signum, frame):
        pass

    @classmethod
    @abstractmethod
    def exit(cls):
        pass


class ComponentMixin(object):
    config: dict = None
    tasks: Queue = None
    suits: List[StepSuit] = []
    pipeline: Pipeline = None
    proxy: Producer = None
