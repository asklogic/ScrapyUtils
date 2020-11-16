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

    do_collect: bool = True

    # def __init__(self):
    #     self.exitcode: int = 0
    #     self.interrupt: bool = False
    #     self.do_collect = True

    @classmethod
    def syntax(cls):
        return '[Command]'

    @classmethod
    def command_config(cls, options):
        """alter command.config

        Args:
            options:
        """
        pass

    @classmethod
    def command_components(cls, steps, processors, options):
        """alter command's components

        Args:
            steps:
            processors:
            options:
        """
        return steps, processors

    @classmethod
    def command_scraper(cls, options) -> None or Callable:
        """alter command.scraper

        Args:
            options:
        """
        return None

    @classmethod
    def command_task(cls, options) -> None or Callable:
        """alter command.tasks

        Args:
            options:
        """
        return None

    @classmethod
    def command_alter(cls, options):
        try:
            # alter config
            cls.config = get_config()
            cls.command_config(options)

            # alter components
            steps, processors = cls.command_components(get_steps(), get_processors(), options)
            set_steps(steps)
            set_processors(processors)

            # alter scraper
            scraper = cls.command_scraper(options)
            if scraper:
                set_scraper_callable(scraper)

            # alter task
            task = cls.command_task(options)
            if task:
                set_task_callable(task)

        except Exception as e:
            log.exception(e, line=3)
            raise Exception('Failed in the initialing of command.')

    @classmethod
    def start(cls, options):
        """command run without blocking.

        Args:
            options:
        """
        exception = options.get('exception')

        # TODO: the delay
        log.info('scraping mission starts in 3 second.')
        sleep(1)
        log.info('scraping mission starts in 2 second.')
        sleep(1)
        log.info('scraping mission starts in 1 second.')
        sleep(1)

        try:
            cls.run(options)
        except Exception as e:
            if exception:
                log.error('Failed in the running of command.')
                log.exception(e, line=3)
            return False
        return True

        # try:
        #     cls.command_collect(options)
        # except Exception as e:
        #     if exception:
        #         log.error('Failed in the collecting of command.', 'Collect')
        #         log.exception(e, line=0)
        #     return False
        #
        # try:
        #     cls.command_initial(options)
        # except Exception as e:
        #     if exception:
        #         log.error('Failed in the initialing of command.', 'Initial')
        #         log.exception(e, line=0)
        #     return False
        #
        # # refactor:
        #
        # if cls.do_collect:
        #     # collect
        #     # config
        #     pass
        #
        # log.info('-----------> command start <-----------')
        # try:
        #     cls.run(options)
        # except Exception as e:
        #     if exception:
        #         log.error('Failed in the initialing of command.')
        #         log.exception(e, line=0)
        #     return False
        # return True

    @classmethod
    @abstractmethod
    def run(cls, options):
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
    def exit(cls):
        pass


class ComponentMixin(object):
    tasks: Queue = None
    suits: List[StepSuit] = []
    pipeline: Pipeline = None
    proxy: Producer = None
