from ScrapyUtils.libs.model import Model, Field


class TaskModel(Model):
    url = Field(convert=str)
    param = Field()
    count = Field(default=0, convert=int)


Task = TaskModel

# class Task(object):
#     url: str
#     param: dict
#     count: int
#
#     def __new__(cls, *args, **kwargs):
#         return TaskModel()

# class TaskModel(Model):
#     url = Field()
#     param = Field()
#     count = Field()
#
#
# class Task(object):
#     url: str
#     param: str
#
#     count: int
#
#     def __new__(cls, *args, **kwargs) -> TaskModel:
#         task = ModelManager.model("TaskModel")
#         task.count = 0
#         return task
