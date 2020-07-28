# a scrapy tools to scrapy data soon

## How to use


#### 1.create
in command line. create a scheme 
``` 
> python trigger.py generate demo

or

> trigger.exe generate demo
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


