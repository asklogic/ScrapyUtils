import unittest
from unittest import TestCase

from base._core import task_run


class do_core_Test(TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass

    # def test_run(self):
    #     pass
        # job = "auir"
        # scheme_list = load_scheme(job)
        #
        # model_list = load_model(job)
        # manager = ModelManager(model_list)
        #
        # task = Task(url=r"https://ip.cn/")
        # scraper = do_prepare(job)
        #
        # from auir import action, model, parse, conserve
        # do_conserve(manager, "IPConserve")
        # self.assertEqual(load_scheme("auir"), [action.testAction, parse.testParse])
        # self.assertEqual(load_model("auir"), [model.testModel])
        # self.assertEqual(do_prepare("auir"), requestScraper)
        # self.assertEqual(do_action(scheme=scheme_list[0], scraper=scraper, manager=manager).count("118.113.125.64"), 1)
        # self.assertEqual(ModelManager(model_list)["testModel"], [])
        # scrapy(scheme_list, manager, task, scraper)
        # self.assertTrue(do_conserve(manager, "IPConserve"))

    def test_functional_run(self):
        task_run("auir")

    def test_core_run(self):
        pass
        # self.assertEqual(load_scheme("auir"), [action.testAction, parse.testParse])
        # self.assertIsInstance(f, firefoxScraper)

        # self.assertEqual(1,2)
        # self.assertIsInstance(DefaultRequestPrepare().do(), baseScraper)
        # self.assertRaises(TypeError, DefaultRequestPrepare().do, None)


class scrapyTest(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
