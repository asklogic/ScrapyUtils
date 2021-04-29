from queue import Queue

from .scheme import Scheme

from ScrapyUtils import configure


class TaskScheme(Scheme):
    @classmethod
    def start(cls):
        tasks = Queue()
        for task in configure.tasks_callable():
            tasks.put(task)

        configure.tasks = tasks

    @classmethod
    def verify(cls) -> bool:
        assert configure.tasks and isinstance(configure.tasks, Queue)
        return True

    @classmethod
    def stop(cls):
        # TODO: dump to save
        pass
