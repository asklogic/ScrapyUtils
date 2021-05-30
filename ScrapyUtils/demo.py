from schemes import *

if __name__ == '__main__':
    root = Root()
    PreloadScheme.target = 'lianjia'
    root.load(PreloadScheme)

    root.load(ComponentsScheme)
    root.load(ScraperScheme)
    root.load(TasksScheme)

    root.exit()
