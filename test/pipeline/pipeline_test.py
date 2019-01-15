import unittest
from typing import Any
from unittest import TestCase

import sys

sys.path.append(r"E:\cloudWF\python\ScrapyUtils")

from base.Container import Container
from base.Process import Process
from base.Model import Model, Field
from base import core
from faker import Faker
import os
import json

f = Faker(locale='zh_CN')


class Pipeline_Test(TestCase):

    def setUp(self) -> None:
        class TestModel(Model):
            name = Field()
            age = Field()

        self.model = TestModel

        class TestProcess(Process):

            def end_process(self):
                pass
                # print("end")
                # time.sleep(5)
                # print("dump finish")

            def process_item(self, model: TestModel) -> Any:
                # print(model.name)
                return model

        class JsonTestProcess(Process):

            def __init__(self):
                super().__init__()
                self.part = 0
                self.name = ""
                self.file_path = ""
                self.limit = 10000
                self.data = []

                self.file_path = r'E:\cloudWF\python\ScrapyUtils\test\pipeline'
                self.name = "test_pipeline"

            def dump_to_file(self):
                file = self.file_path + "\\" + self.name + "-part" + str(self.part) + ".json"
                print(file)
                with open(file, "w") as f:
                    json.dump(self.data[:self.limit], f)
                    print("success dump file")
                self.part += 1
                self.data = self.data[self.limit:]

            def process_item(self, model: Model):
                self.data.append(model.pure_data())

            def end_process(self):
                print("end process! len:", len(self.data))
                while len(self.data) >= self.limit:
                    self.dump_to_file()

            def end_task(self):
                print("end task! len:", len(self.data))
                if self.data:
                    self.dump_to_file()

        # pipeline = Pipeline()
        # pipeline.add_process(TestProcess())
        # core.build_process()

        pipeline = core.build_process([TestProcess, JsonTestProcess])

        self.pipeline = pipeline

        self.container = Container()

    def tearDown(self) -> None:
        pass

    def test_josnPipeline(self):
        return

        self.container.pipeline = self.pipeline

        for i in range(20000):
            m = self.model()
            m.name = f.name()
            m.age = f.random_digit()
            self.container.add(m)

        m = self.model()
        m.name = f.name()
        m.age = f.random_digit()
        self.container.add(m)

        from base.Container import pool
        self.container.dump()

        pool.wait()
        self.pipeline.end_task()
        # 20001个model 10000/json
        # 最后生成3个json

        self.assertTrue(os.path.exists(r"E:\cloudWF\python\ScrapyUtils\test\pipeline\test_pipeline-part0.json"))
        self.assertTrue(os.path.exists(r"E:\cloudWF\python\ScrapyUtils\test\pipeline\test_pipeline-part1.json"))
        self.assertTrue(os.path.exists(r"E:\cloudWF\python\ScrapyUtils\test\pipeline\test_pipeline-part2.json"))

        self.assertEqual(1, 1)

    def test_pipeline_and_model(self):

        import base

        test_config = {
            "job": "test_job",
            "process": "CustomProcess",
            "models": "CustomTestModel"
        }

        config = base.lib.Config(test_config)

        models = core.load_models(config)
        self.assertEqual(len(models), 1)

        default_model = core.load_default_models()
        self.assertEqual(len(default_model), 2)

        current_models = list(set(default_model + models))
        self.assertEqual(len(current_models), 3)

        print([x.__name__ for x in current_models])
        # TODO log model

        process = core.load_process(config)

        import test_job.process
        self.assertEqual(process, [test_job.process.CustomProcess])

        default_process = core.load_default_process()
        self.assertEqual(len(default_process), 2)

        current_process = process + default_process
        self.assertEqual(len(current_process), 3)

        print([x.__name__ for x in current_process])

        # TODO log process

        # task start
        pipeline = core.build_process(current_process, config)

        containers = core.register_containers(current_models, pipeline)

        core.finish(containers, pipeline)
        from base.Container import pool
        pool.wait()

        self.assertTrue(1, 1)


if __name__ == '__main__':
    unittest.main()
