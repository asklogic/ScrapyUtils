# -*- coding: utf-8 -*-
"""Test http server for test mock server.

"""
import sys
import os
import uvicorn
import threading
from fastapi import FastAPI, Request

sys.path.insert(0, os.path.abspath(f'..{os.sep}..{os.sep}..'))

api = FastAPI()


@api.get(r'/test/get')
def test_get(request: Request):
    return 'success mock get.'


t = threading.Thread(target=lambda: uvicorn.run(api, port=9009, debug=True))
t.setDaemon(True)
t.start()

# test url

