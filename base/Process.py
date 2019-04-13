from abc import abstractmethod
from typing import Tuple, List, Dict, Any
from base.Model import Model, ModelManager
from base.lib import ComponentMeta, Component, Setting
from base.log import act


class BaseProcess(Component):
    pass


def target(model: type(Model)):
    def wrapper(func):
        def innerwrapper(*args, **kwargs):
            if not issubclass(model, Model):
                raise TypeError("target must be class")
            if isinstance(args[1], model):
                return func(*args, **kwargs)
            else:
                return True

        return innerwrapper

    return wrapper


class ProcessorMeta(ComponentMeta):

    def __new__(cls, name, bases, attrs: dict):
        if not attrs.get("target"):
            attrs["target"] = Model
        return super().__new__(cls, name, bases, attrs)


class Processor(object, metaclass=ProcessorMeta):
    target: type(Model)
    _active: bool
    _name: str
    data: []

    setting: Setting

    def __init__(self, setting: Setting):
        self.count: int = 0
        self.next: Processor = None
        self.data = []

        self.setting = setting

    @abstractmethod
    def start_task(self, setting: Setting):
        pass

    @abstractmethod
    def start_process(self, number: int, model: str = "Model"):
        pass

    @abstractmethod
    def end_process(self):
        pass

    @abstractmethod
    def end_task(self):
        pass

    @abstractmethod
    def process_item(self, model: Model) -> Any:
        pass


class Pipeline(object):
    head: Processor = None
    processor_list: List[Processor] = []

    def __init__(self, processor_list: List[type(Processor)] = (), setting: Setting = Setting()):
        """
        构建process
        :param processor_list: processor对象列表
        :param settings: config对象中的pipeline键值 默认为空
        """
        self.head: Processor = None
        self.processor_list: List[Processor] = []
        process_count: List[int] = []

        for process in processor_list:
            current_process: Processor = process(setting)
            current_process.start_task(setting)
            self.add_process(current_process)

    def add_process(self, processor: Processor):
        """
        添加processor
        :param processor:
        :return:
        """
        self.processor_list.append(processor)

        current = self.head
        if self.head is None:
            self.head = processor
        else:
            while current.next is not None:
                current = current.next
            current.next = processor

    def process(self, model: Model) -> Tuple[Model, str]:
        """
        处理一个process
        :param model:
        :return:
        """
        index = 0

        current_process = self.head

        last = model

        # result = current_process.process_item(model)
        #
        # # TODO 判定逻辑
        # while current_process.next is not None:
        #     if isinstance(result, Model) :
        #         # 保存此processor返回的model 传至下一个
        #         current_process = current_process.next
        #         index += 1
        #         last = result
        #         result = current_process.process_item(result)
        #     elif bool(result) or result is None:
        #         # 跳过
        #         current_process = current_process.next
        #         index += 1
        #         result = current_process.process_item(last)
        #     elif result is False:
        #         break
        #     else:
        #         break

        result = last
        # fixme 遗留问题
        while current_process is not None:
            if isinstance(result, current_process.target):
                # 保存此processor返回的model 传至下一个

                result = current_process.process_item(last)
                if isinstance(result, Model):
                    last = result
                index += 1
                current_process = current_process.next
            elif not bool(result):
                # 返回False 直接退出

                break
            else:
                # 跳过

                index += 1
                current_process = current_process.next

        return (last, index)

    def feed_model(self, model_name: str, number: int) -> List[Model]:
        """
        feed Model 生成Model
        由ModelManager生成Model 再由processor进行处理(添加各属性
        :param number: 需要生成的model数量
        :param model_name: model 名称
        :return: 返回进过full过滤过的Model 保证Model值都被填满
        """

        list(map(lambda x: x.start_process(number, ModelManager.model_class(model_name)), self.processor_list))

        act.debug("[Pipeline] feed model start. Model: {0}  number: {1}".format(model_name, number))
        result_list: List[Model] = []

        for index in range(number):
            # 构建Model
            pure_model = ModelManager.model(model_name)

            # 处理Model
            result: Model = self.process(pure_model)[0]
            # 短路 None
            if result and result.full():
                result_list.append(result)

        list(map(lambda x: x.end_process(), self.processor_list))
        act.info("[Pipeline] feed model finish. Model: {0}  remained number: {1}".format(model_name, len(result_list)))
        return result_list

    def dump_model(self, data: List[Model]):
        """
        dump model 将得到的model交由processor处理保存
        :param data: model 列表
        :return:
        """
        number = len(data)

        list(map(lambda x: x.start_process(number), self.processor_list))
        # act.debug("[Pipeline] dump Model. Model: {0}  number: {1}".format(data[0]._name, len(data)))

        process_status = [0 for x in self.processor_list]
        for model in data:
            index: int = self.process(model)[1]
            process_status[index - 1] = process_status[index - 1] + 1

        for i in range(len(self.processor_list)):
            act.debug(
                "[Pipeline] " + " ".join([str(process_status[i]), "in", self.processor_list[i].__class__.__name__]))
        # act.info("[Pipeline] dump Model finish.")

        list(map(lambda x: x.end_process(), self.processor_list))

    def end_task(self):
        """
        关闭process
        :return:
        """
        list(map(lambda x: x.end_task(), self.processor_list))
