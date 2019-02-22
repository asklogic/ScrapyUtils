from typing import List, Dict




class Config(object):

    def __init__(self, config_file, config_name: str):
        target_config: dict = getattr(config_file, config_name)

        job = target_config.get("job")
        schemes = target_config.get("schemes")
        models = target_config.get("models")
        prepare = target_config.get("prepare")
        process = target_config.get("process")
        project = target_config.get("project")

        current_model: List[str] = []
        current_process: List[str] = []
        current_project: Dict[str, str] = {}

        # job
        if not job:
            job = config_name

        if (not schemes) and (type(schemes) is not list):
            raise KeyError("Config must set your target scheme list")

        if not prepare:
            prepare = "DefaultPrepare"

        # 如果只有一个就单独添加
        if not models:
            raise KeyError("Config must set your target models list")
        elif not type(models) == list:
            current_model.append(models)
        else:
            current_model = models

        if not process:
            raise KeyError("Config must set your target process list")
        elif not type(process) == list:
            current_process.append(process)
        else:
            current_process.extend(process)

        if not project:
            for project_setting in ("Thread", "Block", "Proxy_Able", "Project_Path"):
                setting = getattr(config_file, project_setting)
                current_project[project_setting] = setting
        else:
            for project_setting in ("Thread", "Block", "Proxy_Able", "Project_Path"):
                current_project[project_setting] = project[project_setting]

        self.job = job
        self.prepare = prepare
        self.schemes = schemes
        self.models = current_model
        self.process = current_process
        self.project = current_project

    job: str
    schemes: List[str]
    models: List[str]
    process: List[str]
    prepare: str
    project: Dict[str, str]


class ComponentMeta(type):
    def __new__(cls, name, bases, attrs: dict):
        attrs["_name"] = name

        if not attrs.get("_active"):
            attrs["_active"] = False

        return type.__new__(cls, name, bases, attrs)
