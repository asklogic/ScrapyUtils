import unittest
from typing import Optional, Union

from ScrapyUtils.components import ProcessorSuit, Processor
from ScrapyUtils.libs import Proxy, Model, Field


class Count(Model):
    count = Field()


class CounterAlpha(Processor):
    count = 0

    def __init__(self) -> None:
        super().__init__()
        self.count = 0

    def process_item(self, model: Model) -> Optional[Union[Model, bool]]:
        self.count += 1


class CounterBeta(Processor):
    count = 0

    def __init__(self) -> None:
        super().__init__()
        self.count = 0

    def process_item(self, model: Model) -> Optional[Union[Model, bool]]:
        self.count += 1


class Break(Processor):

    def process_item(self, model: Model) -> Optional[Union[Model, bool]]:
        return False


ReturnFalse = Break


class ReturnOther(Processor):

    def process_item(self, model: Model) -> Optional[Union[Model, bool]]:
        return []


class ReturnTrue(Processor):

    def process_item(self, model: Model) -> Optional[Union[Model, bool]]:
        return True


class Increase(Processor):

    def process_item(self, model: Count) -> Optional[Union[Model, bool]]:
        model.count += 5


class IncreaseCheck(Processor):

    def process_item(self, model: Count) -> Optional[Union[Model, bool]]:
        if model.count != 5:
            return False


class Error(Processor):
    def process_item(self, model: Model) -> Optional[Union[Model, bool]]:
        assert False


class TargetCheck(Processor):
    target = Proxy

    def process_item(self, model: Model) -> Optional[Union[Model, bool]]:
        assert False


class MethodProcessTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.suit = ProcessorSuit()

    def test_case_not_return(self):
        """No return will continue process flow."""
        self.suit.add_component(CounterAlpha)
        self.suit.add_component(CounterBeta)

        self.suit.process(Count())

        self.assertEqual(len(self.suit.components), 2)

        self.assertEqual(self.suit.components[0].count, 1)
        self.assertEqual(self.suit.components[1].count, 1)

    def test_case_break(self):
        """Return False will break process flow."""
        self.suit.add_component(CounterAlpha)
        self.suit.add_component(ReturnFalse)
        self.suit.add_component(CounterBeta)

        self.suit.process(Count())

        self.assertEqual(self.suit.components[0].count, 1)
        self.assertEqual(self.suit.components[2].count, 0)

    def test_case_return_object(self):
        """Return [] == return None and will continue process flow."""
        self.suit.add_component(CounterAlpha)
        self.suit.add_component(ReturnOther)
        self.suit.add_component(CounterBeta)

        self.suit.process(Count())

        self.assertEqual(self.suit.components[0].count, 1)
        self.assertEqual(self.suit.components[2].count, 1)

    def test_case_return_true(self):
        """Return False will continue process flow."""
        self.suit.add_component(CounterAlpha)
        self.suit.add_component(ReturnTrue)
        self.suit.add_component(CounterBeta)

        self.suit.process(Count())

        self.assertEqual(self.suit.components[0].count, 1)
        self.assertEqual(self.suit.components[2].count, 1)

    def test_case_return_model(self):
        """Return model will modify model."""
        self.suit.add_component(CounterAlpha)
        self.suit.add_component(Increase)
        self.suit.add_component(IncreaseCheck)
        self.suit.add_component(CounterBeta)

        count = Count()
        count.count = 0
        self.suit.process(count)

        self.assertEqual(self.suit.components[0].count, 1)
        self.assertEqual(self.suit.components[3].count, 1)

        self.assertEqual(count.count, 5)

    def test_case_error(self):
        """Method will not except exception"""
        self.suit.add_component(Error)

        with self.assertRaises(AssertionError) as ae:
            self.suit.process(Count())

    def test_case_target_filter_skip(self):
        """Attribute target will filter out model which is not the instance of target model."""

        self.suit.add_component(CounterAlpha)
        self.suit.add_component(TargetCheck)
        self.suit.add_component(CounterBeta)

        self.suit.process(Count())

        self.assertEqual(self.suit.components[0].count, 1)
        self.assertEqual(self.suit.components[2].count, 1)

    def test_case_target_filter(self):
        """And Proxy will skip."""

        self.suit.add_component(TargetCheck)

        with self.assertRaises(AssertionError) as ae:
            self.suit.process(Proxy())


if __name__ == '__main__':
    unittest.main()
