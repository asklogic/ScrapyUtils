# 


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


## 全局profile文件
## pipeline测试 !
### processor组件 !!
### model测试 !!!!

#### component 组件