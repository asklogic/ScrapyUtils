from abc import abstractmethod
from queue import Queue
from typing import List, Callable
from time import sleep
from sys import exit

from ScrapyUtils.components import StepSuit, Pipeline
from ScrapyUtils.libs import Producer
from ScrapyUtils.core import *

from ScrapyUtils.log import basic as log


class Command(object):
    exitcode: int = 0
    interrupt: bool = False
    running: bool = False

    do_collect: bool = True

    config = dict()

    # def __init__(self):
    #     self.exitcode: int = 0
    #     self.interrupt: bool = False
    #     self.do_collect = True

    @classmethod
    def syntax(cls):
        return '[Command]'

    @classmethod
    def command_config(cls, **kwargs):
        """alter command.config

        Args:
            **kwargs:
        """
        pass

    @classmethod
    def command_components(cls, steps, processors, **kwargs):
        """alter command's components

        Args:
            steps:
            processors:
            **kwargs:
        """
        return steps, processors

    @classmethod
    def command_scraper(cls, **kwargs) -> None or Callable:
        """alter command.scraper

        Args:
            **kwargs:
        """
        return None

    @classmethod
    def command_task(cls, **kwargs) -> None or Callable:
        """alter command.tasks

        Args:
            **kwargs:
        """
        return None

    @classmethod
    def command_collect_logout(cls):
        # log.info('========== suit components ===============')
        log.info('Suit Component:')

        steps = get_steps()
        for i in range(len(steps)):
            log.info('({}) - {}'.format(i + 1, steps[i].name))

        # log.info('========== processor components ==========')
        log.info('Processor Components:')

        processors = get_processors()
        for i in range(len(processors)):
            log.info('({}) - {}'.format(i + 1, processors[i].name))

        # log.info('==========================================')

    @classmethod
    def command_collect(cls, options):
        if not cls.do_collect:
            return True

        log.info('-----------> collect start <-----------')
        scheme = options['kwargs'].get('scheme')

        assert collect_scheme_preload(scheme), 'Interrupted in the scheme proload.'

        # config
        cls.config = get_config()
        cls.command_config(**options)

        # alter components
        steps, processors = cls.command_components(get_steps(), get_processors(), **options)
        set_steps(steps)
        set_processors(processors)

        # alter scraper
        scraper = cls.command_scraper(**options)
        if scraper:
            set_scraper_callable(scraper)

        # alter task
        task = cls.command_task(**options)
        if task:
            set_task_callable(task)

        # command collect success:
        cls.command_collect_logout()

        # update options

    @classmethod
    def command_initial(cls, options):
        """
        Args:
            **kwargs:
        """
        if not cls.do_collect:
            return True

        log.info('-----------> initial start <-----------')
        try:
            collect_scheme_initial(**options)

        # command initial failed:
        except AssertionError as ae:
            # TODO: assert error
            log.error("assert error in initializing of command '{}'. ".format(cls.__name__), 'initial')
            log.exception(ae, 0)
            raise Exception('initial failed.')
        # command initial success:
        except Exception as e:
            log.error("some error in initializing of command '{}'. ".format(cls.__name__), 'initial')
            log.exception(e, 0)
            raise Exception('initial failed.')

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
    def start(cls, options):
        """command run without blocking.

        Args:
            **kwargs:

        Returns:

        """
        exception = options.get('exception')

        try:
            cls.command_collect(options)
        except Exception as e:
            if exception:
                log.error('Failed in the collecting of command.')
                log.exception(e, line=0)
            return False
        try:
            cls.command_initial(options)
        except Exception as e:
            if exception:
                log.error('Failed in the initialing of command.')
                log.exception(e, line=0)
            return False

        if options['kwargs'].get('confirm'):
            sleep(1)
            for i in range(3, 0, -1):
                log.info('command start at {}.'.format(i))
                sleep(1)

        log.info('-----------> command start <-----------')
        try:
            cls.run(options)
        except Exception as e:
            if exception:
                log.error('Failed in the initialing of command.')
                log.exception(e, line=0)
            return False
        return True

        # try:
        #     if options.get('confirm'):
        #         sleep(1)
        #         for i in range(3, 0, -1):
        #             log.info('command start at {}.'.format(i))
        #             sleep(1)
        #     log.info('-----------> command start <-----------')
        #
        #     cls.run(options)
        # except AssertionError as ae:
        #     # TODO: assert error
        #     log.error("assert error in processing of command '{}'. ".format(cls.__name__), 'process')
        #     log.exception('Command', ae, 0)
        #
        # except Exception as e:
        #     log.error("some error in processing of command '{}'. ".format(cls.__name__), 'process')
        #     log.exception('Command', e)
        # else:
        #     return True

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
    def paused(cls):
        pass

    @classmethod
    @abstractmethod
    def restart(cls):
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
