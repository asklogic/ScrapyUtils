import unittest
from typing import Optional, Union

from ScrapyUtils.components.process import Process
from ScrapyUtils.libs import Proxy, Model, Field


class Count(Model):
    count = Field(default=0)


class CounterAlpha(Process):
    count = 0

    def __init__(self) -> None:
        super().__init__()
        self.count = 0

    def process_item(self, model: Model) -> Optional[Union[Model, bool]]:
        self.count += 1


class CounterBeta(Process):
    count = 0

    def __init__(self) -> None:
        super().__init__()
        self.count = 0

    def process_item(self, model: Model) -> Optional[Union[Model, bool]]:
        self.count += 1


class ReturnFalse(Process):

    def process_item(self, model: Model) -> Optional[Union[Model, bool]]:
        return False


class ReturnTrue(Process):

    def process_item(self, model: Model) -> Optional[Union[Model, bool]]:
        return True


class ReturnOtherObject(Process):

    def process_item(self, model: Model) -> Optional[Union[Model, bool]]:
        return object


class ReturnOtherEmpty(Process):

    def process_item(self, model: Model) -> Optional[Union[Model, bool]]:
        return []


class ModelIncrease(Process):

    def process_item(self, model: Count) -> Optional[Union[Model, bool]]:
        model.count += 5


class ModelCheck(Process):

    def process_item(self, model: Count) -> Optional[Union[Model, bool]]:
        if model.count >= 5:
            return False


class Error(Process):
    def process_item(self, model: Model) -> Optional[Union[Model, bool]]:
        assert False


class TargetCheck(Process):
    target = Proxy

    def process_item(self, model: Model) -> Optional[Union[Model, bool]]:
        assert False


def build_process_chain(*process: Process):
    for index in range(len(process) - 1):
        process[index].next = process[index + 1]

    return process[0]


class MethodProcessTestCase(unittest.TestCase):

    def test_process_no_return(self):
        """No return will continue process flow."""

        alpha = CounterAlpha()
        beta = CounterBeta()
        head = build_process_chain(alpha, beta)
        head.do_process_linked(Count())

        assert alpha.count == beta.count == 1

    def test_process_interrupt(self):
        """Return False or raise exception will interrupt """

        alpha = CounterAlpha()
        beta = CounterBeta()

        return_false = ReturnFalse()
        error = Error()

        count = Count()

        with self.subTest('return false will interrupt'):
            alpha.count = beta.count = 0
            head = build_process_chain(alpha, return_false, beta)
            head.do_process_linked(count)

            assert alpha.count == 1
            assert beta.count == 0

        with self.subTest('raise exception will interrupt'):
            alpha.count = beta.count = 0
            head = build_process_chain(alpha, error, beta)

            with self.assertRaises(Exception) as e:
                head.do_process_linked(count)

            assert alpha.count == 1
            assert beta.count == 0

    def test_process_continue(self):
        """Return a modified model and other object will continue process chain."""

        alpha = CounterAlpha()
        beta = CounterBeta()

        return_true = ReturnTrue()
        return_empty = ReturnOtherEmpty()
        return_other = ReturnOtherObject()
        increase = ModelIncrease()

        count = Count()

        with self.subTest('return empty object will continue'):
            alpha.count = beta.count = 0
            head = build_process_chain(alpha, return_empty, beta)

            head.do_process_linked(count)

            assert alpha.count == beta.count == 1

        with self.subTest('return True object will continue'):
            alpha.count = beta.count = 0
            head = build_process_chain(alpha, return_true, beta)

            head.do_process_linked(count)

            assert alpha.count == beta.count == 1

        with self.subTest('return other object will continue'):
            alpha.count = beta.count = 0
            head = build_process_chain(alpha, return_other, beta)

            head.do_process_linked(count)

            assert alpha.count == beta.count == 1

        with self.subTest('return True object will continue'):
            alpha.count = beta.count = 0
            head = build_process_chain(alpha, increase, beta)

            head.do_process_linked(count)

            assert alpha.count == beta.count == 1

    def test_modified_model(self):
        """a modified model will pass to next node(Process)"""

        alpha = CounterAlpha()

        head = build_process_chain(ModelCheck(), alpha)

        [head.do_process_linked(Count(count=index)) for index in range(10)]

        assert alpha.count == 5



if __name__ == '__main__':
    unittest.main()
