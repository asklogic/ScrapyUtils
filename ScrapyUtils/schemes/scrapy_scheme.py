# -*- coding: utf-8 -*-
"""Scrapy Scheme.

爬取核心Scheme。当需要的各模块已经实例化后，将会启动具体的爬取逻辑，并提供全局阻塞函数，供主线程阻塞。

步骤:

    1. 启动Adaptor和线程池，
    2. 通过StepSuit生成回调，消费Task对象，把Task对象放入回调中执行爬取。
    3. 检查爬取结果:
        3.1 正确 - 把爬取后的Models放入Pipeline中，完成本次Task。
        3.2 错误 - 把Task放入错误队列或重试。
    4. 直到完成消费Task对象。

Todo:
    * For module TODOs
    
"""

