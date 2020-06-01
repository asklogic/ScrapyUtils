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
@click.option('--confirm', is_flag=True)
def thread(scheme: str, path, line, confirm):
    trigger('thread', scheme=scheme, path=path, line=line, confirm=not confirm)


@click.command()
@click.argument('scheme')
@click.option('type', '--type', default='html')
@click.option('path', '--path', default=os.getcwd(), type=click.Path())
@click.option('line', '--line', default=3)
@click.option('--confirm', is_flag=True)
def download(scheme: str, type, path, line, confirm):
    trigger('download', scheme=scheme, file_type=type, path=path, line=line, confirm=not confirm)


@click.command()
@click.argument('scheme')
@click.option('download', '--download')
@click.option('index', '--index', default=-1)
@click.option('path', '--path', default=os.getcwd(), type=click.Path())
@click.option('line', '--line', default=3)
@click.option('--confirm', is_flag=True)
def parsing(scheme: str, download, index, path, line, confirm):
    trigger('parsing', scheme=scheme, download=download, index=index, path=path, line=line, confirm=not confirm)


@click.command()
@click.argument('scheme')
@click.option('path', '--path', default=os.getcwd(), type=click.Path())
def single(scheme: str, path):
    trigger('single', scheme=scheme, path=path)


@click.command()
@click.argument('scheme')
@click.option('--confirm', is_flag=True)
def generate(scheme: str, confirm):
    trigger('generate', scheme=scheme, confirm=not confirm)


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
