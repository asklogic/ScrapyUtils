import unittest
import sys
from imp import reload
import traceback
import linecache
import os
import faker

f = faker.Faker(locale='zh_CN')

import flask
from flask import render_template
from flask import request

app = flask.Flask(__name__, template_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'mock_templates'))


@app.route('/')
def hello_world():
    return 'Hello World!'


# page
@app.route('/mock/get', methods=['GET'])
def normal_get():
    return render_template(r'MockTemplate.html', info='success info')


@app.route('/mock/failed', methods=['GET'])
def failed_get():
    return render_template(r'MockTemplate.html', info='failed info', failed=True)


from flask import make_response


@app.route('/mock/error')
def failed_403():
    return make_response(render_template(r'MockFailed.html', msg='403 failed'), 403)


@app.route('/mock/failed')
def failed_503():
    return make_response(render_template(r'MockFailed.html', msg='503 failed'), 503)


@app.route('/mock/random/violation')
def violation():
    import random
    if random.randint(0, 100) > 60:
        return make_response(render_template(r'MockTemplate.html', info='success info'), 200)
    else:
        return make_response(render_template(r'MockFailed.html', msg='503 failed'), 503)


@app.route('/mock/random/dynamic')
def dynamic():
    import random

    persons = []
    for i in range(random.randint(4, 10)):
        persons.append(f.name())

    # !
    # if len(persons) < 5:
    #     persons.clear()

    # persons.clear()
    return make_response(render_template(r'MockTemplate.html', info='success info', persons=persons), 200)


# api
import json


@app.route('/mock/header')
def header():
    header_str = json.dumps(dict(request.headers))
    # return make_response(render_template(r'MockMessage.html', message=header_str), 200)
    return header_str


@app.route('/mock/post/data', methods=['POST'])
def data():
    data_str = json.dumps(dict(request.form))
    return data_str


@app.route('/mock/post/json', methods=['POST'])
def _json():
    data_str = json.dumps(dict(request.json))
    return data_str


# @app.route('/mock/post')
# def post():
#     data_str = request.data

if __name__ == '__main__':
    app.run(debug=True, port=8090)
