import unittest


class StepTestCase(unittest.TestCase):
    def test_sample(self):
        from ScrapyUtils.components import Step, Action, Parse, StepSuit

        Step()

    def test_import_action(self):
        import ScrapyUtils.components.step.action

        from ScrapyUtils.components.step.action import Action

    def test_import_parse(self):
        import ScrapyUtils.components.step.parse

        from ScrapyUtils.components.step.parse import Parse

    def test_import_suit(self):
        import ScrapyUtils.components.step.suit

        from ScrapyUtils.components.step.suit import StepSuit


if __name__ == '__main__':
    unittest.main()
