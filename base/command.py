from base.engine import thread_run, single_run
import click
from base.generate.generator import generate as gen


@click.group()
def cli():
    pass


@click.command()
@click.argument('target')
def thread(target: str):
    thread_run(target)
    pass


@click.command()
@click.argument('target')
def single(target: str):
    single_run('target')
    pass


@click.command()
@click.argument('target')
def generate(target: str):
    gen(target)
    pass


cli.add_command(thread)
cli.add_command(single)
cli.add_command(generate)
# def build_run(config_file, args: str):
#     if len(args) < 3:
#         raise KeyError("set correct arguments")
#
#     # config = Config(config_file, args[2])
#     if args[1] == "single":
#         single_run(args[2])
#     elif args[1] == 'thread':
#         thread_run(args[2])
