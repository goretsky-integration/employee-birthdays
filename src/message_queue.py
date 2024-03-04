import contextlib
import datetime
import json
from collections.abc import Iterable

import pika
from pika.adapters.blocking_connection import BlockingChannel

from models import Event

__all__ = (
    'get_message_queue_channel',
    'send_json_message',
    'send_events',
)


@contextlib.contextmanager
def get_message_queue_channel(rabbitmq_url: str) -> BlockingChannel:
    params = pika.URLParameters(rabbitmq_url)
    with pika.BlockingConnection(params) as connection:
        channel = connection.channel()
        channel.queue_declare('telegram-notifications')
        yield channel


def send_json_message(channel: BlockingChannel, event: Event):
    body = event | {'created_at': datetime.datetime.utcnow()}
    channel.basic_publish(
        exchange='',
        routing_key='telegram-notifications',
        body=json.dumps(body, default=str, ensure_ascii=False).encode('utf-8'),
    )


def send_events(channel: BlockingChannel, events: Iterable[Event]):
    for event in events:
        send_json_message(channel, event)
