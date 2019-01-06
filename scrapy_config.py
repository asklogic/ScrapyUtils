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


Thread: int = 20

Block: int = 20

auir = {
    "name": 'auir',
    "allow": [
        'ProxyAction',
        'IpProxyParse'
    ],
    "prepare": "IpProxyPrepare",
    "conserve": "printConserve",
}

scjst = {
    "name": 'auir',
    "allow": [
        'viewStateParse',
        'ReqNextPageAction',
        'ReqProjectParse',
    ],
    "prepare": "ScjstPrepare",
    "conserve": "printConserve",
}

pp = {
    "name": "blink",
    "allow": [
        "ProxyGetAction",
        "NextPageAction",
        "ProjectInfoParse",
    ],
    "prepare": "PP_Prepare",
    "conserve": "ProxyInfoConserve",
}

agent = {
    'name': 'agent',
    'allow': [
        'AgentAction',
        'AgentParse',
    ],
    'prepare': 'AgentPrepare',
    'conserve': 'AgentConserve',
}

scjst_single = {
    'job': 'hope',
    'allow': [
        'xpath',
        'next',
        "xpathParse",
    ],

    'conserve': "hope",
}

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
        'ActionName',
        'xpath',
        'next',
        "xpathParse",
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
