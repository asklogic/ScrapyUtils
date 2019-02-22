from base.Model import TaskModel, ModelManager


class Task(object):
    url: str
    param: str

    count: int

    def __new__(cls, *args, **kwargs) -> TaskModel:
        task = ModelManager.model("TaskModel")
        task.count = 0
        return task