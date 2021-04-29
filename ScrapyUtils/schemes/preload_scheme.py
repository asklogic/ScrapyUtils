from .scheme import Scheme

from ScrapyUtils import configure

from importlib import import_module


class PreloadScheme(Scheme):
    target: str = None

    @classmethod
    def start(cls):
        assert cls.target, 'Need target module.'
        import_module(cls.target)

    @classmethod
    def verify(cls) -> bool:
        assert configure.steps_class
        assert configure.processors_class

        assert configure.tasks_callable
        assert configure.scraper_callable
        return True

    @classmethod
    def stop(cls):
        pass

    def load_context(self):
        pass

    def check_context(self):
        pass
