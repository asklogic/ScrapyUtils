# a scrapy tools to scrapy data soon

## How to use


#### 1.create
in command line. create a scheme 
``` 
> python trigger.py generate demo
```

#### 2. setting (demo/setting.py)
create your task objects.
```python
# generator your tasks in here.

def generate_tasks(**kwargs):
    for i in range(10):
        t = Task(url='http://yoursite.com')
        yield t
```

#### 3. action (demo/action.py)
get task from step 2 and use scraper to download page.
```python
@active
class DemoAction(ActionStep):
    def scraping(self, task: Task):
        scraper: Scraper = self.scraper
        return scraper.get(url=task.url)

    def check(self, content):
        pass
```

#### 4. parsing (demo/parsing.py)
get content from step 3 and parse it, then yield model objects.
```python
@active
class DemoAction(ActionStep):
    def scraping(self, task: Task):
        scraper: Scraper = self.scraper
        return scraper.get(url=task.url)

    def check(self, content):
        pass
```

#### 5. process model (demo/processor.py)
process your model from step 4.
```python
@active
class DemoProcess(Processor):

    def process_item(self, model: Model) -> Any:
        print(model.pure_data)
        return model      
```

### TODO:
1. pipeline to producer?.
2. producer in pool.
3. command 命令单元测试
4. RequestScraper header in flask.
5. command.thread.ScrapyConsumer 单个任务超时 -> 返回以及改为multiprocessing
6. datamodel 单元测试
7. PyUserInput



#### 重构scrapy逻辑

3. consuming:  
3.1 若引发普通异常(访问异常): 代理超时 页面assert失败等 清除缓存并且Task.count=+1
3.2 若引发单次任务超时异常(用户操作卡死): Scraper退出 消除上一个线程影响 _从Pool获取新的Scraper_ 直接关闭线程


## pipeline 保存文件

##### persist 保存文件

##### thread.ScrapyConsumer 退出延时问题
##### collect preload测试 (新建mock scheme) √
##### Pipeline失败的model保存 (config文件路径 文件名字)
##### component的启停测试 √
##### Processor失败的日志打印 √

### block mark in firefox WebDriverWait √
### global and scheme settings √

## thread multiprocessing
