import json

import httpx

from logger import create_logger

__all__ = ('TelegramBotApiConnection',)

logger = create_logger('telegram')


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

        try:
            response_data = response.json()
        except json.JSONDecodeError:
            logger.error(
                'Telegram Bot API connection: Failed to decode JSON',
                extra={'response_text': response.text},
            )
            return

        if not response_data.get('ok', False):
            logger.error(
                'Telegram Bot API connection: Failed to send message',
                extra={'response_data': response_data},
            )
            return

        logger.info(
            'Telegram Bot API connection: Message sent',
            extra={'response_data': response_data},
        )
