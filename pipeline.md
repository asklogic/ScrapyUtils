### pipeline and container

##### abort conserve

#### Container
model收集器 
> 直接从每个线程的manager收集model 超过一定数额则会将gather数量的
model交给pipeline处理

#### Pipeline and Process
> 通过一个类似责任链和管道的模型来处理modle 采用size为1的线程池
解决线程的同步和占用问题 

假设1s 处理20个task 一个task 对应50个model 则1s ==> 1000个model  
默认pipeline 从去重到保存为json 20000个model 发费时间为小于2s

> 数据库需要进行异常处理以及失败的重试