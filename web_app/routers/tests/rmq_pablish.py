import os
import pika

from pika import BlockingConnection
from dotenv import find_dotenv, load_dotenv


class Publisher:
    def __init__(self, broker_config: dict):
        self.config = broker_config

    def publish(self, routing_key, message):
        connection = self.create_connection()
        channel = connection.channel()
        channel.exchange_declare(exchange=self.config['exchange'],
                                 exchange_type='topic',
                                 durable=True)
        channel.basic_publish(exchange=self.config['exchange'],
                              routing_key=routing_key,
                              body=message)
        print(" [x] Sent message %r for %r" % (message, routing_key))

    def create_connection(self) -> BlockingConnection:
        return pika.BlockingConnection(pika.URLParameters(self.config['url']))


load_dotenv(find_dotenv())

url = os.environ.get('AMQP_URL', "amqp://guest:guest@rabbitmq:5672/")

config = {
    'url': url,
    'exchange': 'manga_tracker'
}

if __name__ == "__main__":
    publisher = Publisher(config)
    msg = '1'
    print(url)
    publisher.publish('new_page', msg)
