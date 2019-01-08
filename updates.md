### 记录修改类型

##### 19.1.1
> TODO  
> 修改load 增加可以通过自带的name字段来进行load  
> 修改generator 默认之生存action parse model三个模板  X
> 重构项目结构  
> 移动老代码   
> 重构 修改各组件方法 成为类方法  
> 修改日志类  X
> 重构Scraper   
> 重构Action  
> 添加多线程支持  

Done:
> Scraper 基类
> RequestsScraper 已经测试 
> 重构Scraper   
> 重构Action  
> 添加多线程支持  
> 重构 修改各组件方法 成为类方法  
> 移动老代码   
> 修改load 增加可以通过自带的name字段来进行load  

### 19.1.4
> log 日志类重构    
> 添加异常处理机制  
> 添加代理  done
> generator设置  
> 修改Model处理逻辑   
> 添加Container   

bugs:
```
无法加载 default conserve   done
model manager 注册名字错误 Model  
xpath 解析错误 (解决)  
xpath 添加 默认scheme添加   
```


#### 19.1.6
feature todo list
> 注册各类Container  
> 自带Count / Proxy / Failed Container 和 Model(s) Container    
> Container 和 Conserve的互通  
> 各个组件加载 重构engine逻辑  
> 添加Check函数 启动  
> 修改日志类  
> generator设置   
> 添加异常处理机制   

#### 19.1.7
Done
> 注册各类Container  
> 自带Count / Proxy / Failed Container 和 Model(s) Container  (Proxy完成
> Container 和 Conserve的互通  
> 各个组件加载 重构engine逻辑  

TODO feature
> generator设置   
> 修改日志类  
> 添加Check函数 启动  
> xpath Hidden 等自带parse函数
> model name加载和注册
> model Filed问题


bugs:
```
不存在parse 等文件时 会出错
conserve 进程冲突
```

其他:
conserve 与 container 比较 冲突?
