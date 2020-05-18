import signal
import sys

from .entity import ComponentMixin, Command
from . import command_map

from base.core import *
from base.exception import CommandExit
from base.log import set_syntax, Wrapper as log


def trigger(command_name: str, **kwargs):
    # get command class
    command: ComponentMixin or Command = command_map[command_name]

    set_syntax(command.syntax())

    # register signal
    # TODO: windows and linux
    signal.signal(signal.SIGTERM, command.signal_callback)
    signal.signal(signal.SIGINT, command.signal_callback)
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

            # initial scheme
            if kwargs.get('confirm'):
                input('Press any key to continue.')

            collect_scheme_initial()

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

    except CommandExit as ex:
        log.info('CommandExit interrupt.', 'System', 'Interrupt')

    except Exception as e:
        command.failed()
        log.exception('Command', e)

    finally:
        log.info('command exiting...', 'System', 'Processing')

        command.exit()
        log.info('command exited.', 'System', 'Processing')

    sys_exit(command.exitcode)


def sys_exit(exitcode: int):
    sys.exit(exitcode)
