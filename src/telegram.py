import json

import httpx
import structlog.stdlib
from structlog.contextvars import bound_contextvars

__all__ = ('TelegramBotApiConnection',)

log = structlog.stdlib.get_logger('app')


class TelegramBotApiConnection:

    def __init__(
            self,
            *,
            token: str,
    ):
        self.__token = token

    @property
    def base_url(self) -> str:
        return f'https://api.telegram.org/bot{self.__token}'

    def send_message(self, *, chat_id: int, text: str) -> None:
        url = f'{self.base_url}/sendMessage'
        request_data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}

        # No need to create connection pool, because we have only one request
        # to the Telegram Bot API in whole app.
        response = httpx.post(url=url, json=request_data)

        with bound_contextvars(
                request_data=request_data,
                status=response.status_code,
        ):

            try:
                response_data = response.json()
            except json.JSONDecodeError:
                log.error(
                    'Telegram Bot API connection: Failed to decode JSON',
                    response_text=response.text,
                )
                return

            if not response_data.get('ok', False):
                log.error(
                    'Telegram Bot API connection: Failed to send message',
                    response_data=response_data,
                )
                return

            log.info(
                'Telegram Bot API connection: Message sent',
                response_data=response_data,
            )
