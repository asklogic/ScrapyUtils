import unittest
import socket
import time

from base.listen import Listener, stop_listener, get_output, _socket_connect


class TestCaseListener(unittest.TestCase):
    def test_demo(self):
        listener = Listener()

        assert listener.port == 52000
        assert listener.stop is False

        assert stop_listener(52000) is True

        # need some time to receive
        time.sleep(0.2)
        assert listener.stop is True

    def test_init_port(self):
        listener = Listener(52002)

        assert listener.port == 52002
        assert listener.stop is False


    def test_property_socket(self):
        listener = Listener()

        assert listener.socket
        assert isinstance(listener.socket, socket.socket)

    def test_property_active(self):
        listener = Listener()

        assert listener.active is True

    def test_method_set_output(self):
        listener = Listener()

        output = 'lianjia-' + str(int(time.time())) + '.out'
        listener.set_output(output)

    def test_method_wait_to_start(self):
        listener = Listener()
        assert listener.wait is False

        # listener.wait_to_start()

    def test_function_get_output(self):
        listener = Listener()
        output = 'lianjia-' + str(int(time.time())) + '.out'
        listener.set_output(output)

        print('port is ', listener.port)
        assert get_output(listener.port) == output

    def test_function_stop_listener(self):

        listener = Listener()

        assert listener.is_alive()

        stop_listener(listener.port)

        time.sleep(1)

        assert listener.is_alive() is False


    @unittest.skip
    def test_property_active_false(self):
        listener = Listener()
        listener.socket.close()
        assert listener.active is False


if __name__ == '__main__':
    unittest.main()
