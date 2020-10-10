import socket
import threading
import time

from .log import common as log
from .log import basic


def _socket_connect(msg, port, timeout=0.1):
    """
    Args:
        msg:
        port:
        timeout:
    """
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


def change_state(port):
    """
    Args:
        port:
    """
    data = _socket_connect(msg=3, port=port)
    return bool(int(data))


def start_listener(port):
    """
    Args:
        port:
    """
    data = _socket_connect(msg=1, port=port)
    if data == 'start listener.':
        return True
    return False


def stop_listener(port):
    """
    Args:
        port:
    """
    data = _socket_connect(msg=0, port=port)

    if data == 'stop listener.':
        return True
    return False


def get_output(port) -> str or False:
    """
    Args:
        port:
    """
    data = _socket_connect(msg=2, port=port, timeout=1)
    return data


def port_connect_test(port):
    """
    Args:
        port:
    """
    data = _socket_connect(msg=9, port=port)
    if isinstance(data, str):
        return True
    return False


def port_bind_test(port):
    """
    Args:
        port:
    """
    s = socket.socket()
    s.settimeout(0.1)
    host = '127.0.0.1'

    try:
        s.bind((host, port))
    except OSError as ose:
        if 'WinError 10048' in str(ose):
            return True
    else:
        return False
    finally:
        s.close()


# FIXME: connect reply
class Listener(threading.Thread):
    # socket
    port: int = 52000
    socket: socket.socket

    # property
    output: str = ''

    def __init__(self, port=52000, output: str = 'None'):

        """
        Args:
            port:
            output (str):
        """
        threading.Thread.__init__(self)

        self.socket = socket.socket()

        while port_bind_test(port) and port_connect_test(port) and port < 52100:
            port += 1

        self.setDaemon(True)

        # property
        self.output = str(output)
        self.port = port

        self.state = True

    @property
    def active(self):
        return not self.socket._closed

    def block_to_start(self, block_state=True, timeout=300):

        """
        Args:
            block_state:
            timeout:
        """
        while self.state == block_state and timeout != 0:
            timeout -= 1
            time.sleep(0.2)
        self.state = not block_state

    @property
    def finished(self):
        """case 1: before thread start. is_alive -> False & active -> True case
        2: thread running. is_alive -> True & active -> True case 3: thread
        done. is_alive -> False * active -> False

        case 1 & 2 -> False. case 3 -> True
        """
        if self.is_alive() or self.active:
            return False
        return True

    def stop(self):
        return stop_listener(self.port)

    def run(self) -> None:
        self.socket.bind((('127.0.0.1', self.port)))
        self.socket.listen(5)

        connect_loop_flag = True

        basic.info('port: {}.'.format(self.port), 'Listener')

        while connect_loop_flag:
            connect, addr = self.socket.accept()
            try:
                command = connect.recv(1024)
                while True:
                    if command == b'0':
                        log.info('stop listener.', 'Listener')
                        connect.send(b'stop listener.')
                        break
                    elif command == b'9':
                        connect.send(b'scraping scheme')
                    elif command == b'2':
                        log.info('get output file', 'Listener')
                        connect.send(self.output.encode('utf-8'))
                    elif command == b'1':
                        self.wait = True
                        log.info('start listener', 'Listener')
                        connect.send(b'start listener.')
                    elif command == b'3':
                        self.state = not self.state
                        # if self.state:
                        #     log.info('command paused. listener block: {}.'.format(self.state), 'Listener')
                        # else:
                        #     log.info('command start. listener block: {}.'.format(self.state), 'Listener')

                        connect.send(str(int(self.state)).encode('utf-8'))
                    else:
                        connect.send(b'not a registered state.')

                    command = connect.recv(1024)

            except Exception as e:
                pass
                # print('connect closed.')
            else:
                connect_loop_flag = False
            finally:
                connect.close()

        self.socket.close()

    def __del__(self):
        self.socket.close()
