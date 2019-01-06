from base.lib import Prepare, Task


class Scjst_basePrepare(Prepare):
    
    @classmethod
    def task_prepared(cls):
        task = Task()
        task.url = "http://xmgk.scjst.gov.cn/QueryInfo/Project/ProjectList.aspx"
        task.param = 10
        yield task
