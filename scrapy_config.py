import os
import os.path as path
#
#
#
#
#
#

# Global Setting

# Job config
# auir = {
#     "name": 'auir',
#     "allow": [
#         'IpTestAction',
#         'JustForTestParse'
#     ],
#     "prepare": "TestPrepare",
#     "conserve": "IPConserve",
# }

Project_Path = path.dirname(path.realpath(__file__))
Assets_Path = os.path.join(Project_Path, "assets")


Thread: int = 30
Block: int = 0.05
# Block: int = 2

Proxy_Able = True
# Proxy_Able = False




ProxyInfo = {
    'job': 'hope',
    'allow': [
        'xpath',
    ],
    'conserve': "hope",

}

scjst_thread = {
    'job': 'hope',
    'allow': [
        'xpath',
        'next',
        " ",
    ],
    "models": [
        "ViewstateModel",
        "ProjectModel",
        "ProjectInfoModel",
    ],
    'prepare': "xmgk",
    'conserve': "hope",
}

xxgx_thread = {
    'job': 'hope',
    'allow': [
        'queryname',
        'QueryParse',
        'querycode',
        'QueryParse',

        # 'xpath',
        # "xpathParse",
    ],
    "prepare": "query",
    'conserve': "nope",
}

test_conf = {
    "job": "hope",
    "allow": [
        "xpath",
    ],
    "models": [
        'ProxyInfoModel'
    ],
    "prepare": "test_thread_prepare",
    "conserve": "test_conserve",
}


re_scjst_base = {
    'job': 'scjst_base',
    'allow': [
        'xpath',
        'next',
        # 'xpath',
        'ProjectBaseParse',
    ],
    "models": [
        "ViewstateModel",
        "ProjectBaseModel",
    ],
    'prepare': "ProjectBasePrepare",
    'conserve': "re_save_project_base",
}

query_scjst_xmgk = {
    'job': 'scjst_base',
    'allow': [
        'query_name',
        'QueryParse',
        'query_code',
        'QueryParse',

    ],
    "models": [
        "ProjectIDModel",
        # "ProjectBaseModel",
    ],
    'prepare': "QueryProjectPrepare",
    'conserve': "QueryConserve",
}

