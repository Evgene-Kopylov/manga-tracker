import os
from typing import Any

import pika
from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import find_dotenv, load_dotenv
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from db.models import Page
from db.session import SessionLocal
from manga_parser import MangaParser

load_dotenv(find_dotenv())

session = SessionLocal()
parser = MangaParser()


class InstaMangaParser:
    """
    parsing target page on request from RabbitMQ network

    Main methods:
    - start() — launch listening.
    """

    def __init__(self):
        self.exchange = 'manga_tracker'
        self.discord_webhook_url = os.environ.get('DISCORD_WEBHOOK_URL', 'http://None')
        self.debug = True if os.getenv('DEBUG', '0') in ('1', 'true',
                                                         'yes') else False
        self.amqp_url = os.environ.get('AMQP_URL', 'amqp://guest:guest@localhost:5672/')
        self.routing_key = os.environ.get('ROUTING_KEY', 'new_page')

    def start(self) -> None:
        """
        launch listening.
        """
        channel = self.connect()
        self.log("RabbitMQ exchange for manga-tracker"
                 f"{self.routing_key=}'\n"
                 "Waiting for messages...")
        channel.start_consuming()

    def log(self,
            comment: Any = '',
            important: bool = False,
            msg: str = ''
            ) -> int:
        """
        Sends errors logs to Discord server

        @param comment: optional comment to main message
        @param important: importance flag, if True, the message
                          will be sent regardless of debug mode
        @param msg: message from RabbitMQ network
        @return: discord response status code
        """
        print(comment)
        if not self.debug and not important:
            return 200
        webhook = DiscordWebhook(url=self.discord_webhook_url)
        embed = DiscordEmbed(title="INFO", description=comment, color='3498db')
        line = f'some info on msg {msg}'
        embed.add_embed_field(name='line', value=line, inline=True)
        embed.set_timestamp()
        webhook.add_embed(embed)
        response = webhook.execute()
        return response.status_code

    def connect(self) -> BlockingChannel:
        """
        Connect to manga-tracker RabbitMQ channel
        exchange `topic`

        :return: channel
        """
        connection = pika.BlockingConnection(pika.URLParameters(self.amqp_url))
        channel = connection.channel()
        channel.exchange_declare(exchange=self.exchange,
                                 exchange_type='topic',
                                 durable=True)
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(queue=queue_name,
                           exchange=self.exchange,
                           routing_key=self.routing_key)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue_name, self.callback)
        return channel

    def callback(self, ch: BlockingChannel, method: Basic.Deliver,
                 properties: BasicProperties, body: bytes) -> None:
        """
        On-message actions

        @param ch: channel
        @param method: internal methods
        @param properties:
        @param body: message body
        """
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(body)
        routing_key = method.routing_key
        print(f"{routing_key=}")
        msg = body.decode('utf-8')
        comment = self.msg_is_valid(msg)
        if comment != 'OK':
            self.log(comment=comment, msg=msg)
            return

        page = session.query(Page).filter_by(id=int(msg)).first()
        parser.start(page)

        comment = f'{page.id=} {page.name=}' if page else f'{page=}'
        self.log(comment=comment, important=True)
        return

    @staticmethod
    def msg_is_valid(msg: str) -> str:
        """
        Checks if message is valid

        @param msg: message to check
        @return: 'OK' if valid
        """
        if msg.isdigit():
            return 'OK'
        else:
            return 'not digit'


if __name__ == "__main__":
    mpar = InstaMangaParser()
    mpar.start()
