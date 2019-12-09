import pika

from pika_client import util


class Session:
    def __init__(self, username=None, password=None, url=None, port=None, payload_callback=None):
        self.username = username
        self.password = password
        self.url = url
        self.port = port
        self.payload_callback = payload_callback
        self.connection = None
        self.channel = None
        self.queue = None
        self.custom_logger = util.logger('pika_client')

    def connect(self):
        credentials = pika.PlainCredentials(self.username, self.password)
        parameters = pika.ConnectionParameters(self.url, self.port, '/', credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def run(self, queue=None, prefetch=10):
        self.connect()
        self.queue = queue
        self.channel.basic_qos(prefetch_count=prefetch)
        self.channel.basic_consume(queue=queue, on_message_callback=self.callback)
        self.channel.start_consuming()

    def callback(self, channel, method, properties, body):
        payload = util.transform_payload(body)
        self.custom_logger.info('Incoming message: %s' % payload)
        try:
            self.payload_callback(payload)
            self.reconnect(self.ack, channel, method, payload)
        except Exception as ex:
            self.reconnect(self.nack, channel, method, ex)

    def ack(self, channel, method, payload):
        channel.basic_ack(delivery_tag=method.delivery_tag)
        self.custom_logger.info('Acknowledged %s' % payload)

    def nack(self, channel, method, ex):
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        self.custom_logger.error('Callback error: %s' % ex)

    def reconnect(self, useful_work, *args):
        try:
            useful_work(*args)
        except (pika.exceptions.ChannelWrongStateError, pika.exceptions.ConnectionClosed,
                pika.exceptions.ConnectionClosedByBroker, pika.exceptions.ConnectionWrongStateError,
                pika.exceptions.AMQPConnectionError, pika.exceptions.AMQPHeartbeatTimeout) as e:
            self.custom_logger.info('Reconnecting...')
            self.run(queue=self.queue)

    def close(self):
        try:
            self.channel.stop_consuming()
            self.connection.close()
        except pika.exceptions.StreamLostError:
            pass
