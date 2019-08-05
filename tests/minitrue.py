import unittest
import sys
from imp import reload
import traceback
import linecache
import os

import flask
from flask import render_template
from flask import request

# suite = unittest.TestSuite()
# suite.addTest(test_scraping.TestScraping('test_core_scraping'))
# # 执行测试
#
#
# runner = unittest.TextTestRunner(stream=sys.stdout,verbosity=2, buffer=False)
# runner = unittest.TextTestRunner(verbosity=2, buffer=False)
# runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2, buffer=True)
# runner = unittest.TextTestRunner(verbosity=2, buffer=True)
#
# # runner.run(suite)
#


# runner = unittest.TextTestRunner(verbosity=2, buffer=True)
# while True:
#     import time
#
#     try:
#         target = __import__('tests.core.test_scraping', fromlist=['core'])
#         reload(target)
#
#         runner.run(unittest.TestLoader().loadTestsFromTestCase(getattr(target,'TestScraping')))
#
#     except SyntaxError as se:
#
#         trace = se.__traceback__
#
#         while trace.tb_next is not None:
#             trace = trace.tb_next
#
#         print('SyntaxError in  line X: ', linecache.getline(se.filename, se.lineno), end='')
#
#         print('code:')
#
#         [print('line [{0}]:{1}'.format(se.lineno-3+x, linecache.getline(se.filename, se.lineno-3+x)), end='') for x in range(7)]
#
#         pass
#
#
#
#     for i in range(1,4):
#         print(i)
#         time.sleep(1)
#     os.system('cls')

app = flask.Flask(__name__, template_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'mock_templates'))


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/mock/get')
def normal_get():
    return render_template(r'MockTemplate.html', info='success info')


from flask import make_response


@app.route('/mock/error')
def failed_403():
    return make_response(render_template(r'MockFailed.html', msg='403 failed'), 403)


@app.route('/mock/failed')
def failed_503():
    return make_response(render_template(r'MockFailed.html', msg='503 failed'), 503)


import json


@app.route('/mock/header')
def header():
    header_str = json.dumps(dict(request.headers))
    # return make_response(render_template(r'MockMessage.html', message=header_str), 200)
    return header_str


@app.route('/mock/data')
def data():
    data_str = json.dumps(dict(request.data))
    return data_str

    # return make_response(render_template(r'MockMessage.html', message=data_str), 200)



def newspeak():
    app.run(port=8090, use_reloader=False)
