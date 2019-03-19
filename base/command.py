from base.engine import _single_run, _thread_run, thread_run, single_run
from base.lib import Config


def build_run(config_file, args: str):
    if len(args) < 3:
        raise KeyError("set correct arguments")

    # config = Config(config_file, args[2])
    if args[1] == "single":
        single_run(args[2])
    elif args[1] == 'thread':
        thread_run(args[2])
