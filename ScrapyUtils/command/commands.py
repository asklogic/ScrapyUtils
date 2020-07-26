import os
import click

from ScrapyUtils.engine import trigger


@click.group()
def cli():
    pass


@click.command()
@click.argument('scheme')
@click.option('path', '--path', default=os.getcwd(), type=click.Path())
@click.option('line', '--line', default=3)
@click.option('-p', '--port', 'port', type=int)
@click.option('-c', '--confirm/--no-confirm', 'confirm', is_flag=True, default=False)
@click.option('-b', '--background/--no-background', 'background', is_flag=True, default=True)
@click.option('-l', '--log/--no-log', 'log', is_flag=True, default=False)
def thread(scheme: str, path, line, confirm, port, background, log):
    """
    Args:
        scheme (str):
        path:
        line:
        confirm:
        port:
        background:
        log:
    """
    trigger(command='thread', scheme=scheme, path=path, line=line, confirm=confirm, port=port, background=background,
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
@click.option('line', '--line', default=3)
@click.option('download', '--download')
@click.option('-p', '--port', 'port', type=int)
@click.option('-c', '--confirm/--no-confirm', 'confirm', is_flag=True, default=False)
@click.option('-b', '--background/--no-background', 'background', is_flag=True, default=True)
@click.option('-l', '--log/--no-log', 'log', is_flag=True, default=False)
def download(scheme: str, path, line, download, confirm, port, background, log):
    """
    Args:
        scheme (str):
        path:
        line:
        confirm:
        port:
        background:
        log:
    """
    trigger(command='download', scheme=scheme, path=path, download=download, line=line, confirm=confirm, port=port,
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
@click.option('line', '--line', default=3)
@click.option('download', '--download')
@click.option('index', '--index', default=-1)
@click.option('-c', '--confirm/--no-confirm', 'confirm', is_flag=True, default=False)
@click.option('-b', '--background/--no-background', 'background', is_flag=True, default=True)
@click.option('-l', '--log/--no-log', 'log', is_flag=True, default=False)
def parsing(scheme: str, path, line, download, index, confirm, background, log):
    """
    Args:
        scheme (str):
        path:
        line:
        download:
        index:
        confirm:
        background:
        log:
    """
    trigger(command='parsing', scheme=scheme, path=path, line=line, download=download, index=index, confirm=confirm,
            background=False,
            log=log)


@click.command()
@click.argument('scheme')
@click.option('path', '--path', default=os.getcwd(), type=click.Path())
def single(scheme: str, path):
    """
    Args:
        scheme (str):
        path:
    """
    trigger('single', scheme=scheme, path=path)


@click.command()
@click.argument('scheme')
@click.option('-c', '--confirm/--no-confirm', 'confirm', is_flag=True, default=False)
def generate(scheme: str, confirm):
    """
    Args:
        scheme (str):
        confirm:
    """
    trigger(command='generate', scheme=scheme, confirm=confirm, background=False)


@click.command()
@click.argument('target')
def check(target: str):
    """
    Args:
        target (str):
    """
    trigger('check', target=target)


cli.add_command(thread)
cli.add_command(single)
cli.add_command(generate)
cli.add_command(check)
cli.add_command(download)
cli.add_command(parsing)
