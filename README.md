# 


### TODO:
1. pipeline to producer?.
2. producer in pool.
3. thread in commnad 重构
4. RequestScraper header in flask.
5. 拆分command.Command
6. proxy in producer.


#### 重构scrapy逻辑

3. consuming:  
3.1 若引发普通异常(访问异常): 代理超时 页面assert失败等 清除缓存并且Task.count=+1
3.2 若引发单次任务超时异常(用户操作卡死): Scraper退出 消除上一个线程影响 从Pool获取新的Scraper
6. exit: join instead of loop.