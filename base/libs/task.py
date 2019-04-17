from base.components.model import ModelManager, Model, Field





class TaskModel(Model):
    url = Field()
    param = Field()
    count = Field()

class Task(object):
    url: str
    param: str

    count: int

    def __new__(cls, *args, **kwargs) -> TaskModel:
        task = ModelManager.model("TaskModel")
        task.count = 0
        return task