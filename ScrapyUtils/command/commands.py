import os
import click

from ScrapyUtils.engine import trigger


@click.group()
def cli():
    pass


@click.command()
@click.argument('scheme')
@click.option('path', '--path', default=os.getcwd(), type=click.Path())
@click.option('-p', '--port', 'port', type=int)
@click.option('-c', '--confirm/--no-confirm', 'confirm', is_flag=True, default=False)
@click.option('-b', '--background/--no-background', 'background', is_flag=True, default=True)
@click.option('-l', '--log/--no-log', 'log', is_flag=True, default=False)
def thread(scheme: str, path, confirm, port, background, log):
    """Default Mode."""

    trigger(command='thread', scheme=scheme, path=path, confirm=confirm, port=port, background=background,
            log=log)


# @click.command()
# @click.argument('scheme')
# @click.option('type', '--type', default='html')
# @click.option('path', '--path', default=os.getcwd(), type=click.Path())
# @click.option('line', '--line', default=3)
# @click.option('--confirm', is_flag=True)
# def download(scheme: str, type, path, line, confirm):
#     trigger('download', scheme=scheme, file_type=type, path=path, line=line, confirm=confirm)

@click.command()
@click.argument('scheme')
@click.option('path', '--path', default=os.getcwd(), type=click.Path())
@click.option('download', '--download')
@click.option('-p', '--port', 'port', type=int)
@click.option('-c', '--confirm/--no-confirm', 'confirm', is_flag=True, default=False)
@click.option('-b', '--background/--no-background', 'background', is_flag=True, default=True)
@click.option('-l', '--log/--no-log', 'log', is_flag=True, default=False)
def download(scheme: str, path, download, confirm, port, background, log):
    """Download the HTML or other content."""

    trigger(command='download', scheme=scheme, path=path, download=download, confirm=confirm, port=port,
            background=background,
            log=log)


# @click.command()
# @click.argument('scheme')
# @click.option('download', '--download')
# @click.option('index', '--index', default=-1)
# @click.option('path', '--path', default=os.getcwd(), type=click.Path())
# @click.option('line', '--line', default=3)
# @click.option('--confirm', is_flag=True)
# def parsing(scheme: str, download, index, path, line, confirm):
#     trigger('parsing', scheme=scheme, download=download, index=index, path=path, line=line, confirm=confirm)

@click.command()
@click.argument('scheme')
@click.option('path', '--path', default=os.getcwd(), type=click.Path())
@click.option('download', '--download')
@click.option('index', '--index', default=-1)
@click.option('-c', '--confirm/--no-confirm', 'confirm', is_flag=True, default=False)
@click.option('-b', '--background/--no-background', 'background', is_flag=True, default=True)
@click.option('-l', '--log/--no-log', 'log', is_flag=True, default=False)
def parsing(scheme: str, path, download, index, confirm, background, log):
    """Parsing from the download folder."""
    trigger(command='parsing', scheme=scheme, path=path, download=download, index=index, confirm=confirm,
            background=False,
            log=False)


@click.command()
@click.argument('scheme')
@click.option('path', '--path', default=os.getcwd(), type=click.Path())
def single(scheme: str, path):
    """[TODO]"""
    trigger('single', scheme=scheme, path=path)


@click.command()
@click.argument('scheme')
@click.option('-c', '--confirm/--no-confirm', 'confirm', is_flag=True, default=False)
def generate(scheme: str, confirm):
    """Generate a tempalte."""
    trigger(command='generate', scheme=scheme, confirm=confirm, background=False)


@click.command()
@click.argument('target')
def check(target: str):
    """[TODO]"""
    trigger('check', target=target)


cli.add_command(thread)
cli.add_command(single)
cli.add_command(generate)
cli.add_command(check)
cli.add_command(download)
cli.add_command(parsing)
