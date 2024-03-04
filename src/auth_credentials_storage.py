import httpx
import structlog.stdlib
from structlog.contextvars import bound_contextvars

from new_types import AuthCredentialsStorageConnectionHttpClient

__all__ = ('AuthCredentialsStorageConnection',)

log = structlog.stdlib.get_logger('app')


class AuthCredentialsStorageConnection:

    def __init__(
            self,
            http_client: AuthCredentialsStorageConnectionHttpClient,
    ):
        self.__http_client = http_client

    def get_accounts(self) -> httpx.Response:
        url = '/accounts/'

        log.debug('Fetching accounts: sending request')
        response = self.__http_client.get(url)
        log.debug(
            'Fetching accounts: received response',
            status=response.status_code,
        )

        return response

    def get_cookies(self, account_name: str) -> httpx.Response:
        url = '/auth/cookies/'
        request_query_params = {'account_name': account_name}

        with bound_contextvars(request_query_params=request_query_params):
            log.debug('Fetching account cookies: sending request')
            response = self.__http_client.get(
                url=url,
                params=request_query_params,
            )
            log.debug(
                'Fetching account cookies: received response',
                status=response.status_code,
            )

        return response
