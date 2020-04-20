import unittest
import sys
import threading
import time

from base.libs.threads import BaseThread


class MyTestCase(unittest.TestCase):

    def test_property_is_alive(self):
        """
        start thread in __init__
        threading.Thread property : alive
        """
        base = BaseThread()
        assert base.is_alive() is True

    def test_property_daemon(self):
        """
        threading.Thread property : daemon
        """

        base = BaseThread()
        assert base.daemon is True

    def test_property_event_isset(self):
        """
        BaseThreading property : event
        """
        base = BaseThread()
        assert base.event.is_set() is False

        base.event.set()

        assert base.event.is_set() is True

        base.event.clear()
        assert base.event.is_set() is False

    def test_init_event_default(self):
        """
        parameter : event
        critical: same event. start and stop keep the same action.s
        """

        base1 = BaseThread()
        base2 = BaseThread()

        assert id(base1.event) == id(base2.event)

    def test_init_event(self):
        """
        property : _stopped_event
        """
        import threading
        event = threading.Event()

        base = BaseThread(event)

        assert base.event is event
        assert base._stopped_event is event
        assert id(base.event) == id(event)

    def test_init_event_assert(self):
        with self.assertRaises(Exception) as e:
            BaseThread(object())

        assert 'need event instance.' in str(e.exception)

    def test_init_kw_name(self):
        """
        property kwargs : name
        """
        n = BaseThread(**{'name': 'custom_name'})
        assert n.getName() == 'custom_name'

    @unittest.skip
    def test_method_run(self):
        """
        stop at once.
        TODO: fixme
        """

        class Custom(BaseThread):
            def run(self):
                raise Exception()

        custom = Custom()

        assert custom.is_alive() is False
        custom.start()
        assert custom.is_alive() is True

        # blink.
        import time
        time.sleep(0.1)
        assert custom.is_alive() is False

    def test_method_stop(self):
        """
        block till stopped is True
        """
        base = BaseThread()
        base.start(True)

        assert base.stopped is False
        assert base.event.is_set() is True

        base.stop(True)
        assert base.stopped is True
        assert base.event.is_set() is False

    def test_method_stop_not_block(self):
        base = BaseThread()
        base.start()

        assert base.is_alive() is True
        assert base.event.is_set() is True
        assert base.stopped is False

        base.stop(False)
        assert base.stopped is False
        assert base.event.is_set() is False

        # not block.
        time.sleep(1 + 0.01)
        assert base.stopped is True

    def test_method_start(self):
        base = BaseThread()

        assert base.stopped is True
        assert base.event.is_set() is False

        base.start(True)

        assert base.stopped is False
        assert base.event.is_set() is True

    def test_method_start_not_block(self):
        base = BaseThread()

        assert base.event.is_set() is False
        assert base.stopped is True

        base.start()
        # after event.set() stopped be False immediately
        # assert base.stopped is True
        assert base.stopped is False
        assert base.event.is_set() is True


if __name__ == '__main__':
    unittest.main()
