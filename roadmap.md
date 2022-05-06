### 初版

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



### 完全版