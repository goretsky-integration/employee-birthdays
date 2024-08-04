import httpx

from logger import create_logger
from new_types import AuthCredentialsStorageConnectionHttpClient

__all__ = ('AuthCredentialsStorageConnection',)

logger = create_logger('app')


class AuthCredentialsStorageConnection:

    def __init__(
            self,
            http_client: AuthCredentialsStorageConnectionHttpClient,
    ):
        self.__http_client = http_client

    def get_accounts(self) -> httpx.Response:
        url = '/accounts/'

        logger.debug('Fetching accounts: sending request')
        response = self.__http_client.get(url)
        logger.debug(
            'Fetching accounts: received response',
            extra={'status': response.status_code},
        )

        return response

    def get_cookies(self, account_name: str) -> httpx.Response:
        url = '/auth/cookies/'
        request_query_params = {'account_name': account_name}

        logger.debug('Fetching account cookies: sending request')
        response = self.__http_client.get(
            url=url,
            params=request_query_params,
        )
        logger.debug(
            'Fetching account cookies: received response',
            extra={'status': response.status_code},
        )

        return response
