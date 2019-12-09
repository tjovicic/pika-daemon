from unittest.mock import MagicMock
import unittest
import pika

from pika_client import Session


class TestRunner(unittest.TestCase):

    def test_calling_nack_after_throwing_exception(self):
        session = Session()
        session.payload_callback = MagicMock()
        session.payload_callback.side_effect = Exception('boom')

        session.nack = MagicMock()
        session.ack = MagicMock()
        channel = MagicMock()
        method = MagicMock()

        session.callback(channel, method, None, b'')

        assert session.nack.call_count == 1
        assert session.ack.call_count == 0

    def test_calling_ack(self):
        session = Session()
        session.payload_callback = MagicMock()

        session.nack = MagicMock()
        session.ack = MagicMock()
        channel = MagicMock()
        method = MagicMock()

        session.callback(channel, method, None, b'')

        assert session.nack.call_count == 0
        assert session.ack.call_count == 1

    def test_reconnecting(self):
        session = Session()
        session.payload_callback = MagicMock()
        session.run = MagicMock()
        session.nack = MagicMock()

        method = MagicMock()
        channel = MagicMock()
        channel.basic_ack.side_effect = pika.exceptions.AMQPConnectionError('test')

        session.callback(channel, method, None, b'')

        assert session.run.call_count == 1
        assert session.nack.call_count == 0


if __name__ == '__main__':
    unittest.main()
