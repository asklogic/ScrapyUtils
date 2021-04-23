from .scheme import Scheme

from ScrapyUtils import configure

from importlib import import_module


class PreloadScheme(Scheme):
    target: str = None

    def deploy(self):
        assert self.target, 'Need target module.'
        import_module(self.target)

    def verify(self) -> bool:
        assert configure.steps_class
        assert configure.processors_class

        assert configure.tasks_callable
        assert configure.scraper_callable
        return True

    def exit(self):
        pass

    def load_context(self):
        pass

    def check_context(self):
        pass
