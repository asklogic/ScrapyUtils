# class BaseException(Exception):
#     pass


class HTTPStatusException(Exception):

    # def __init__(self, status_code, title:str) -> None:
    #     super(HTTPStatusException, self).__init__()
    # self.args = (status_code,title)

    def __init__(self, *args):
        self.args = ('custom',)
        self.status_code = args[0]
        self.title = args[1]


class ConfigureException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class SchemeException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class CommandInterruptedException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
