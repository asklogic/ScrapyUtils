import os
from logging import getLogger
from typing import Dict

from ScrapyUtils.generate import templates
from string import Template

logger = getLogger('generate')

templates_folder_path: str = os.path.join(os.path.dirname(__file__), 'templates')

generator_mapper = {
    "web_action.template": "action_template",
    "parse_action.template": "parser_template",
    "processor.template": "process_template",
    "model.template": "model_template",
    "settings.template": "settings_template",
    '__init__.template': 'init_template',
}

templates_mapper: Dict[str, str] = {}
"""文件名和模板内容的映射"""

for key, value in generator_mapper.items():
    template_file_path = os.path.join(templates_folder_path, key)

    with open(template_file_path, encoding='utf-8') as f:
        templates_mapper[key] = f.read()


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
    for template_name, template_content in templates_mapper.items():
        # 创建文件绝对路径
        component_path = os.path.join(path, template_name)

        if not os.path.isfile(component_path):
            with open(os.path.join(path, f'{template_name.split(".")[0]}.py'), "w") as f:
                template = Template(template_content)

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
