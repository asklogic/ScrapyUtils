import signal
import ctypes
import sys

from .entity import ComponentMixin, Command
from . import command_map

from base.core import *
from base.exception import CommandExit


def trigger(command_name: str, **kwargs):
    # get command class
    """
    Args:
        command_name (str):
        **kwargs:
    """
    command: ComponentMixin or Command = command_map[command_name]

    set_syntax(command.syntax())

    # register signal
    # TODO: windows and linux
    # FIXME: signal in windows(ctrl + c锛塩an not exit FirefoxScraper
    signal.signal(signal.SIGTERM, command.signal_callback)
    signal.signal(signal.SIGINT, command.signal_callback)

    # ucrtbase = ctypes.CDLL('ucrtbase')
    # c_raise = ucrtbase['raise']
    # signal.signal(signal.SIGINT, lambda *args: c_raise(signal.SIGTERM))

    log.info('starting command {}'.format(command.__name__), 'System', 'Processing')
    # TODO: try - catch
    try:
        # collect. -> core.collect
        if command.do_collect:
            # preload scheme
            collect_scheme_preload(kwargs.get('scheme'))

            # config
            command.config = get_config()
            command.command_config(**kwargs)

            # alter components
            steps, processors = command.command_components(get_steps(), get_processors(), **kwargs)
            set_steps(steps)
            set_processors(processors)

            # alter scraper
            scraper = command.command_scraper(**kwargs)
            if scraper:
                set_scraper_callable(scraper)

            # alter task
            task = command.command_task(**kwargs)
            if task:
                set_task_callable(task)

            command.command_collect_logout()
            # initial scheme
            collect_scheme_initial(**kwargs)

            # TODO: refactor
            command.suits = get_suits()
            command.tasks = get_tasks()
            command.pipeline = get_pipeline()
            command.proxy = get_proxy()

            # TODO: proxy start.
            if command.proxy:
                command.proxy.start()

        log.debug('command running...', 'System', 'Processing')

        command.run(kwargs)

        log.debug('command finish.', 'System', 'Processing')
    # except KeyboardInterrupt as ke:
    #     log.info('KeyboardInterrupt interrupt.', 'Interrupt')

    except CommandExit as ce:
        log.info('CommandExit interrupt.', 'Interrupt')

    except AssertionError as ae:
        log.exception('Command', ae, 0)

    except Exception as e:
        command.failed()
        log.exception('Command', e)

    finally:
        log.info('command exiting...', 'System', 'Exit')

        command.exit()
        log.info('command exited.', 'System', 'Exit')

    sys_exit(command.exitcode)


def sys_exit(exitcode: int):
    """
    Args:
        exitcode (int):
    """
    sys.exit(exitcode)
