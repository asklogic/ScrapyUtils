from tests.minitrue import app


def two_minute_hate():
    app.run(port=8090, use_reloader=False)

