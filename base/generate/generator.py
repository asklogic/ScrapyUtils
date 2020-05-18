import os

from base.generate import templates
from string import Template

generator_mapper = {
    "action.py": "action_template",
    "parse.py": "parse_template",
    "processor.py": "process_template",
    "model.py": "model_template",
    # "prepare.py": "prepare_template",
    "settings.py": "settings_template"

}

init_template = """from base.core.collect import collect_steps, collect_processors, collect_settings

from . import action, parse, processor, settings

steps_class = collect_steps(action, parse)
processors_class = collect_processors(processor)
config, tasks_callable, scraper_callable = collect_settings(settings)
"""


def create_folder(path: str):
    """
    create target folder and __init__.py file

    :param target: target name
    """

    # create data folder
    target_data_path = os.path.join(path, 'data')
    if not os.path.isdir(target_data_path):
        os.makedirs(target_data_path)

    target_data_path = os.path.join(path, 'download')
    if not os.path.isdir(target_data_path):
        os.makedirs(target_data_path)

    target_data_path = os.path.join(path, 'tasks')
    if not os.path.isdir(target_data_path):
        os.makedirs(target_data_path)

    # init file
    with open(os.path.join(path, "__init__.py"), "w") as f:
        f.writelines(init_template)


def create_components(path: str):
    target = os.path.basename(path)
    for component in generator_mapper:
        component_path = os.path.join(path, component)

        if not os.path.isfile(component_path):
            with open(os.path.join(path, component), "w") as f:
                template = Template(getattr(templates, generator_mapper[component]))

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
    # dir_generator(target)
    # component_generate(target)
