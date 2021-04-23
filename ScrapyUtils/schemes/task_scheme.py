from queue import Queue

from .scheme import Scheme

from ScrapyUtils import configure


class TaskScheme(Scheme):
    def deploy(self):
        tasks = Queue()
        for task in configure.tasks_callable():
            tasks.put(task)

        configure.tasks = tasks

    def verify(self) -> bool:
        assert configure.tasks and isinstance(configure.tasks, Queue)
        return True

    def exit(self):
        # TODO: dump to save
        pass
