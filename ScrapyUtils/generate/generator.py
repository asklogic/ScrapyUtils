import os
from logging import getLogger

from ScrapyUtils.generate import templates
from string import Template

logger = getLogger('generate')

generator_mapper = {
    "action.py": "action_template",
    "processor.py": "process_template",
    "model.py": "model_template",
    "settings.py": "settings_template",
    '__init__.py': 'init_template',
}

for key, value in generator_mapper.items():
    generator_mapper[key] = getattr(templates, value)


def create_folder(path: str):
    """create target folder and __init__.py file

    Args:
        path (str):
    """

    # create data folder
    target_data_path = os.path.join(path, 'data')
    if not os.path.isdir(target_data_path):
        os.makedirs(target_data_path)
        logger.debug(f'Created folder: {target_data_path}')

    target_data_path = os.path.join(path, 'download')
    if not os.path.isdir(target_data_path):
        os.makedirs(target_data_path)
        logger.debug(f'Created folder: {target_data_path}')

    target_data_path = os.path.join(path, 'tasks')
    if not os.path.isdir(target_data_path):
        os.makedirs(target_data_path)
        logger.debug(f'Created folder: {target_data_path}')


def create_components(path: str):
    """创建文件"""
    # 目标路径
    target = os.path.basename(path)

    # 遍历模板字典
    for component in generator_mapper:
        # 创建文件绝对路径
        component_path = os.path.join(path, component)

        if not os.path.isfile(component_path):
            with open(os.path.join(path, component), "w") as f:
                template = Template(generator_mapper[component])

                code = template.substitute(class_name=target.capitalize())
                f.writelines(code)
            logger.debug(f'Created file: {component_path}')

        else:
            logger.error(f'Exist file named: {component_path}')


def remove(target):
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
    create_folder(target)
    create_components(target)
