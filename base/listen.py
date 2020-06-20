import socket
import threading
import time

from base.log import Wrapper as logger


def _socket_connect(msg, port, timeout=0.1):
    msg = str(msg)
    assert isinstance(msg, str), 'msg must str'

    s = socket.socket()
    s.settimeout(timeout)
    host = '127.0.0.1'

    try:
        s.connect((host, port))
        s.send(msg.encode('utf-8'))
        data = s.recv(1024).decode('utf-8')
    except Exception as e:
        return False
    else:
        return data
    finally:
        s.close()


def block_listener(port):
    data = _socket_connect(msg=3, port=port)
    return bool(int(data))


def start_listener(port):
    data = _socket_connect(msg=1, port=port)
    if data == 'start listener.':
        return True
    return False


def stop_listener(port):
    data = _socket_connect(msg=0, port=port)

    if data == 'stop listener.':
        return True


def get_output(port) -> str or False:
    data = _socket_connect(msg=2, port=port, timeout=1)
    return data


def port_connect_test(port):
    data = _socket_connect(msg=9, port=port)
    if isinstance(data, str):
        return True
    return False


# FIXME: connect reply
class Listener(threading.Thread):
    block: bool = True
    output: str = None
    port: int = 52000
    socket: socket.socket
    wait: bool = False

    def __init__(self, port=52000):
        threading.Thread.__init__(self)

        _socket = socket.socket()

        host = '127.0.0.1'
        while port_connect_test(port) and port < 52100:
            port += 1

        _socket.bind((host, port))
        _socket.listen(5)

        self.setDaemon(True)
        # property
        # TODO: refactor. too many property
        self.block = True
        self.output = 'output'
        self.port = port
        self.socket = _socket
        self.wait = False

        self.start()

    @property
    def active(self):
        return not self.socket._closed

    def set_output(self, output: str):
        self.output = output

    def wait_to_start(self, timeout=100):
        while not self.wait:
            timeout -= 1
            time.sleep(0.2)
        assert timeout, 'wait timeout'

    def run(self) -> None:
        connect_loop_flag = True
        # print('start listening.', self.port)

        while connect_loop_flag:
            connect, addr = self.socket.accept()
            try:
                command = connect.recv(1024)
                while True:
                    if command == b'0':
                        logger.info('stop listener', 'Listener')
                        connect.send(b'stop listener.')
                        break
                    elif command == b'9':
                        print('test_connect')
                        connect.send(b'scraping scheme')
                    elif command == b'2':
                        logger.info('get output file', 'Listener')
                        connect.send(self.output.encode('utf-8'))
                    elif command == b'1':
                        self.wait = True
                        logger.info('start listener', 'Listener')
                        connect.send(b'start listener.')
                    elif command == b'3':
                        self.block = not self.block
                        if self.block:
                            logger.info('command paused. listener block state: {}'.format(self.block), 'Listener')
                        else:
                            logger.info('command start. listener block state: {}'.format(self.block), 'Listener')

                        connect.send(str(int(self.block)).encode('utf-8'))
                    else:
                        connect.send(b'no state.')

                    command = connect.recv(1024)

            except Exception as e:
                pass
                # print('connect closed.')
            else:
                connect_loop_flag = False
                print('connect exit.')
            finally:
                connect.close()

    def __del__(self):
        self.socket.close()
