## Command 

#### trigger

trigger负责执行整个命令,控制命令的整体执行流程.

在整个的trigger执行过程中,异常是可控的,分为各个stage.
每个stage有其自己的异常处理操作,以应对未知的异常以及响应强行退出信号.


> 首先执行命令查找操作,如果dict中不存在,则抛出KeyError.

存在命令 获取命令类 再进行下一步stage操作

> stage操作分为: 准备 初始化 执行 退出 销毁

stage各阶段
1. 准备: 代码检查 操作确认
2. 初始化: collect操作 各项操作激活
3. 执行: 执行
4. 退出: 关闭各项Scraper 等待Pipeline保存
5. 销毁: 直接销毁各对象 sys.exit


 