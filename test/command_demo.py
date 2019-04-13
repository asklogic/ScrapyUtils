import click


@click.command()
def single_test(target):
    print("here!")
    print(target)


@click.command()
@click.argument('name')
def invoke_test(name = 'default'):
    print('arg' , name)
    pass


@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s!' % name)



if __name__ == '__main__':
    # single_test()
    invoke_test()
    # hello()
    pass