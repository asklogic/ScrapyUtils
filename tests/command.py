import click


@click.group()
def telescreen():
    '''
    Telescreen - automatic run unittest.
    '''
    pass


@click.command()
@click.argument('file_name')
@click.option('-f', '--folder', 'folder', default='tests', show_default=True, prompt='Detect in folder:')
@click.option('-t', '--type', 'type', default='py', show_default=True, prompt='File suffix:')
def watch(file_name: str, folder: str, type: str):
    '''
    tracking files change and run unittest python file.
    '''
    print(file_name)
    print(folder)
    print(type)
    pass


@click.command()
@click.option('-f', '--folder', 'folder', default='tests')
def discover(folder):
    '''
    [TODO] run all unittest in folder.
    '''
    pass


telescreen.add_command(discover)
telescreen.add_command(watch)

if __name__ == '__main__':
    telescreen()
