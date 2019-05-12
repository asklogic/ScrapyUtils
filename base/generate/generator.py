import os
from os import path
from base.log import act

from base.generate import templates
from string import Template

from base.core import PROJECT_PATH

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


def dir_generator(job_name: str):
    target_path = os.path.join(PROJECT_PATH, job_name)

    # create target folder and __init__.py file
    if not os.path.isdir(target_path):
        # folder
        os.makedirs(target_path)

        # init file
        with open(os.path.join(target_path, "__init__.py"), "w") as f:
            pass

    # create data folder
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


def generate(target: str):
    dir_generator(target)
    component_generate(target)


# refact

def create_folder(target: str, data: bool = True) -> bool:
    """
    create target folder and __init__.py file

    :param target:
    :return: if exist target folder,return False.
    """
    target_path = os.path.join(PROJECT_PATH, target)

    if not os.path.isdir(target_path):
        # folder
        os.makedirs(target_path)

        # create data folder
        if data:
            target_data_path = os.path.join(target_path, 'data')
            if not os.path.isdir(target_data_path):
                os.makedirs(target_data_path)

        # init file
        with open(os.path.join(target_path, "__init__.py"), "w") as f:
            pass

        return True
    return False


def create_components(target: str):
    target_path = os.path.join(PROJECT_PATH, target)

    for component in generator_mapper:
        component_path = os.path.join(target_path, component)
        if not os.path.isfile(component_path):
            with open(os.path.join(target_path, component), "w") as f:
                template = Template(getattr(templates, generator_mapper[component]))
                # code = template.substitute(class_name="".join([target[0:1].upper(), target[1:]]))
                code = template.substitute(class_name=target.capitalize())
                f.writelines(code)


def remove(target):
    import os

    # files
    for file in list(os.walk(target))[0][2]:
        file_path = os.path.join(os.getcwd(), target, file)
        os.remove(file_path)

    # folders (empty
    for folder in list(os.walk(target))[0][1]:
        folder_path = os.path.join(os.getcwd(), target, folder)
        os.rmdir(folder_path)

    # target itself
    os.rmdir(os.path.join(os.getcwd(), target))


if __name__ == '__main__':
    target = "ProxyKuai"
    dir_generator(target)
    component_generate(target)
