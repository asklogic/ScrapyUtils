from tests.minitrue import app
import os
import sys

def two_minute_hate():
    app.run(port=8090, use_reloader=False)


# test configure

tests_path = os.path.dirname(__file__)
project_path = os.path.dirname(tests_path)


# test scheme root path

schemes_path = os.path.join(tests_path, 'mock_schemes')
sys.path.append(schemes_path)


