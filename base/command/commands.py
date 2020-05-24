import os
import click

from .process import trigger


@click.group()
def cli():
    pass


@click.command()
@click.argument('scheme')
@click.option('path', '--path', default=os.getcwd(), type=click.Path())
@click.option('line', '--line', default=3)
def thread(scheme: str, path, line):
    trigger('thread', scheme=scheme, path=path, line=line, confirm=True)


@click.command()
@click.argument('scheme')
@click.option('type', '--type', default='html')
@click.option('path', '--path', default=os.getcwd(), type=click.Path())
@click.option('line', '--line', default=3)
def download(scheme: str, type, path, line):
    trigger('download', scheme=scheme, file_type=type, path=path, line=line, confirm=True)


@click.command()
@click.argument('scheme')
@click.option('download', '--download')
@click.option('index', '--index', default=-1)
@click.option('path', '--path', default=os.getcwd(), type=click.Path())
@click.option('line', '--line', default=3)
def parsing(scheme: str, download, index, path, line):
    trigger('parsing', scheme=scheme, download=download, index=index, path=path, line=line, confirm=True)


@click.command()
@click.argument('scheme')
@click.option('path', '--path', default=os.getcwd(), type=click.Path())
def single(scheme: str, path):
    trigger('single', scheme=scheme, path=path)


@click.command()
@click.argument('scheme')
def generate(scheme: str):
    trigger('generate', scheme=scheme, confirm=True)


@click.command()
@click.argument('target')
def check(target: str):
    trigger('check', target=target)


cli.add_command(thread)
cli.add_command(single)
cli.add_command(generate)
cli.add_command(check)
cli.add_command(download)
cli.add_command(parsing)
