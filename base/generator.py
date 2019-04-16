import os
from os import path
from base.log import act

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


def job_generation(job: str):
    job = job.strip()
    if not path.exists(os.path.join(PROJECT_PATH, job)) or path.isfile(os.path.join(PROJECT_PATH, job)):
        act.warning("same name path has existed: " + os.path.join(PROJECT_PATH, job))
        os.mkdir(os.path.join(PROJECT_PATH, job))

    for file in generator_list:
        # 如果存在 就不覆写
        if path.exists(os.path.join(PROJECT_PATH, job, file)):
            act.warning("exist file: " + os.path.join(PROJECT_PATH, job, file))
            continue
        else:
            file_generation(os.path.join(PROJECT_PATH, job), file)
            act.debug("create file: " + os.path.join(PROJECT_PATH, job, file))

            code_generation(file, job)
            act.info("generated file: " + os.path.join(PROJECT_PATH, job, file))


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


def dir_generator(job_name: str):
    target_path = os.path.join(PROJECT_PATH, job_name)

    if not os.path.isdir(target_path):
        os.makedirs(target_path)
        with open(os.path.join(target_path, "__init__.py"), "w") as f:
            pass

    target_data_path = os.path.join(target_path, 'data')
    if not os.path.isdir(target_data_path):
        os.makedirs(target_data_path)


def component_generate(job_name: str):
    target_path = os.path.join(PROJECT_PATH, job_name)

    for component in generator_mapper:
        component_path = os.path.join(target_path, component)
        if not os.path.isfile(component_path):
            with open(os.path.join(target_path, component), "w") as f:
                template = Template(getattr(templates, generator_mapper[component]))
                code = template.substitute(class_name="".join([job_name[0:1].upper(), job_name[1:]]))
                f.writelines(code)


def overwrite(job_name):
    target_path = os.path.join(PROJECT_PATH, job_name)

    for component in generator_mapper:
        component_path = os.path.join(target_path, component)
        if os.path.isfile(component_path):
            with open(os.path.join(target_path, component), "w") as f:
                template = Template(getattr(templates, generator_mapper[component]))

                code = template.substitute(class_name="".join([job_name[0:1].upper(), job_name[1:]]))
                f.writelines(code)


if __name__ == '__main__':
    target = "TestMockServer"
    dir_generator(target)
    component_generate(target)


