import os
from os import path

from base import templates

PROJECT_PATH = os.path.dirname(os.getcwd())

generator_list = [
    "action.py",
    "parse.py",
    "conserve.py",
    "model.py",
    "prepare.py",
]

mapper = {
    "action.py": "action_template",
    "parse.py": "parse_template",
    "conserve.py": "conserve_template",
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
    if not os.path.isfile(os.path.join(file_path, file)):
        # os.mknod(os.path.join(file_path, "action.py"))
        with open(os.path.join(file_path, file), "w") as f:
            pass
    pass


def code_generation(file, job):
    template = getattr(templates, mapper[file])
    code = template.format(job.capitalize())

    with open(os.path.join(PROJECT_PATH, job, file), "a") as f:
        f.writelines(code)

def config_generation(job):
    template = getattr(templates, "config_template")
    code = template.format(job, job.capitalize())

    with open(os.path.join(PROJECT_PATH, "scrapy_config.py"), "a") as f:
        f.writelines(code)


if __name__ == '__main__':
    pass
    job_generation("ProxyInfo")
    config_generation("ProxyInfo")