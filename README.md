#ScrapyUtils


### TODO


1. check 命令
2. step 命令
3. 重构 single 命令(check 基础)
4. 重构日志类 基于component
5. 分解Component基类 加上单元测试
6. 自带组件测试套件


#### def scrapy

> 在scraping / parsing 中的错误 检测 scheme名字+  错误类型 + 代码内容 日志输出
> 在scrap_check 中的断言问题 + 自带检测错误 + 自定义检测错误 同上   
> 保证在scrapy函数中不会抛出其他异常

#### 自定义异常
> 1. Exception.py 包含类型 解析 储存三大类问题 覆盖 prepare + scheme + processor 三大组件(model自动略过)
> 2. 和日志类配套


#### 日志类 
> 1. 兼容异常类


#### 命令 
> 1. 模板类 
  



