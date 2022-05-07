### Demo版本

1. 解析Action和Processor, 读取设置  
   1.1 读取Action, 构建ActionSuit  
   1.2 读取Processor, 构建ProcessorSuit  
   1.3 读取Setting
2. 启动线程池, 正常执行Action  
   2.1 构建线程池  
   2.2 读取Task  
   2.3 构建Scraper, 分配于不同线程  
   2.4 执行主要循环
3. 回收Model, 执行Processor  
   3.1 执行Suit处理Model

### 升级优化流程

1. 分离下载和解析命令
2. 重写工具类
3. 优化并整理打包脚本
4. 修改基于Selenium的Scraper并且完成测试
5. 删除老代码并且完成一些遗留工作
6. 完成Watch模式
7. 完成3个不同论坛的抓取样例
8. 0.1版本开发完毕

#### 后续开发目标

1. 