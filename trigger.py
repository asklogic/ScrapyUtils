import sys
import os
from ScrapyUtils.command.commands import cli

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    cli()
