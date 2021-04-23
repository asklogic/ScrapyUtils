from schemes import *

if __name__ == '__main__':
    root = Root()
    PreloadScheme.target = 'lianjia'
    root.load(PreloadScheme)

    root.load(InitialScheme)
    root.load(ScraperScheme)
    root.load(TaskScheme)

    root.exit()
