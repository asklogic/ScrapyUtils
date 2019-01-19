#ScrapyUtils


### 项目结构

1. assets 静态资源 (redis)
2. tools 主要类库
    1.logger 日志
    2.requestBase 项目基本类(requester scraper)
    3.requestException 项目异常类 (基本没动)
    4.requestParser 项目解析类
    5.utils 项目工具类(数据库连接等)
  
3. origin 存放actions和parser
4. extend selenium扩展 (TODO)
5. main.py 项目入口
6. settings.py 项目配置文件
7. demo.py test.py 测试
8. 其他 临时测试文件


#### TODO

√线程同步 (临界资源 )
守护线程 - 数据保存 数据库连接,全局变量,日志等
√解析 (更快捷) xpath - items
execl √json csv container

重构parser action遍历过程

√proxy缓存池修复
√失败url保存 - 需要守护线程
requestsScraper 修复

√追加url(增量爬取) main注册器

√重构engine
√添加自定义异常
优化主程序
proxy何时更新?
日志类修复
√安全退出
√添加自定义item类型

action url判断
action任务完成判断


### 异常处理机制

1. 抛出自定义异常 


19.1.18
