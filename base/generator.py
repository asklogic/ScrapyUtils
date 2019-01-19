import os
from os import path

from base import templates
from string import Template

PROJECT_PATH = os.path.dirname(os.getcwd())

generator_list = [
    "action.py",
    "parse.py",
    "process.py",
    "model.py",
    "prepare.py",
]

generator_mapper = {
    "action.py": "action_template",
    "parse.py": "parse_template",
    "process.py": "process_template",
    "model.py": "model_template",
    "prepare.py": "prepare_template",
}




def job_generation(job):
    if not path.exists(os.path.join(PROJECT_PATH, job)) or path.isfile(os.path.join(PROJECT_PATH, job)):
        os.mkdir(os.path.join(PROJECT_PATH, job))

    for file in generator_list:
        file_generation(os.path.join(PROJECT_PATH, job), file)

        code_generation(file, job)


def file_generation(file_path, file):
    """
    生成文件
    :param file_path:
    :param file:
    :return:
    """
    if not os.path.isfile(os.path.join(file_path, file)):
        with open(os.path.join(file_path, file), "w") as f:
            pass


def code_generation(file, job):
    """
    生成并且写入模板
    :param file:
    :param job:
    :return:
    """
    template = Template(getattr(templates, generator_mapper[file]))

    code = template.substitute(class_name=job.capitalize())

    with open(os.path.join(PROJECT_PATH, job, file), "a") as f:
        f.writelines(code)

def config_generation(job):
    template = getattr(templates, "config_template")
    code = template.format(job, job.capitalize())

    with open(os.path.join(PROJECT_PATH, "scrapy_config.py"), "a") as f:
        f.writelines(code)


if __name__ == '__main__':
    job_generation("generator_test")
    # config_generation("ProxyInfo")