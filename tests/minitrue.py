import unittest
import sys
from imp import reload
import traceback
import linecache
import os

import flask
from flask import render_template

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


def newspeak():
    app.run(port=8090)
