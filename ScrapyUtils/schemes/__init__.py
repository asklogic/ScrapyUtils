# -*- coding: utf-8 -*-
"""The scheme for ScrapyUtils.

自动化爬取工具系统自带的各项步骤/方案（scheme）。

系统提供一个Root管理类，管理一个进程下面的各项组件。

一个样例:
    系统需要启动Redis模块作为爬取任务来源，将会执行以下步骤：

    1. 尝试连接Redis数据库，判断连接状态。

    2. 开启Redis连接，替换系统原有的Queue数据源。

    3. 系统退出时再进行数据持久化操作。

系统提供Scheme类，Scheme提供了启动前校验，启动函数，退出函数和引用上下文作为Scheme组件间的交互和集成。
Scheme模仿了常见Service模式的设计方法，把一部分模块服务化，解耦各模块间的依赖。

Todo:
    * ROOT装饰器化。

"""
from .scheme import Root, Scheme

from .preload_scheme import PreloadScheme
from .components_scheme import ComponentsScheme
from .scraper_scheme import ScraperScheme

# logger

from ScrapyUtils.log import build_defalut_logger

state_logger = build_defalut_logger('scheme_state',
                                    format_str="[%(state)s in '%(method)s'] - %(message)s",
                                    time_format='%H:%M:%S')

load_logger = build_defalut_logger('scheme_load',
                                   format_str='(%(levelname)s) %(message)s',
                                   time_format='%H:%M:%S')
