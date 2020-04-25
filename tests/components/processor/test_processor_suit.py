import unittest
from typing import Any

from base.components import Processor, Pipeline
from base.components.pipeline import ProcessorSuit
from base.libs import Model, Field


class Blank(Processor):

    def process_item(self, model: Model) -> Any:
        pass

    def __init__(self, config: dict = None):
        super().__init__(config)


class MockInitFailed(Processor):

    def __init__(self, config: dict = None):
        super().__init__(config)
        raise Exception('mock exception.')


class MockOnStart(Processor):

    def on_start(self):
        self.start_sign = []


class MockOnStartFailed(Processor):

    def on_start(self):
        raise Exception('raise mock on_start exception.')


class MockOnExit(Processor):
    def on_exit(self):
        self.exit_sign = []


class MockOnExitFailed(Processor):
    def on_exit(self):
        raise Exception('raise mock on_exit exception.')


config = {
    'info': 'information',
}


class TestProcessorSuit(unittest.TestCase):
    def test_demo(self):
        suit = ProcessorSuit([])

    def test_function_init(self):
        suit = ProcessorSuit([Blank])

        assert suit.components[0].count == 0
        assert suit.components[0].data == []

    def test_function_init_config(self):
        suit = ProcessorSuit([Blank], config)

        assert suit.components[0].config == config
        assert suit.components[0].config is config

    def test_function_init_failed(self):
        suit = ProcessorSuit([Blank, MockInitFailed])

        assert len(suit.components) == 1

    def test_function_suit_start(self):
        suit = ProcessorSuit([Blank, MockOnStart])
        suit.suit_start()

        assert suit.components[1].start_sign == []

    def test_function_suit_start_failed(self):
        suit = ProcessorSuit([Blank, MockOnStartFailed, MockOnStart])

        with self.assertRaises(Exception) as e:
            suit.suit_start()
        # assert 'Processor MockOnStartFailed start failed.' in str(e.exception)
        assert 'interrupt' in str(e.exception)

    def test_function_suit_exit(self):

        suit = ProcessorSuit([Blank, MockOnExit])
        suit.suit_start()
        suit.suit_exit()


        assert suit.components[1].exit_sign == []

    def test_function_suit_exit_failed(self):
        suit = ProcessorSuit([Blank, MockOnExitFailed ,MockOnExit])
        suit.suit_start()
        suit.suit_exit()

        assert suit.components[2].exit_sign == []


if __name__ == '__main__':
    unittest.main()
