from collections.abc import Generator

import structlog.stdlib
from structlog.contextvars import bound_contextvars

from new_types import DodoISConnectionHttpClient, HTML

__all__ = ('DodoISConnection',)

log = structlog.stdlib.get_logger('app')


class DodoISConnection:

    def __init__(self, http_client: DodoISConnectionHttpClient):
        self.__http_client = http_client

    def iter_employee_birthdays(
            self,
            *,
            cookies: dict[str, str],
    ) -> Generator[HTML, None, None]:
        url = '/OfficeManager/EmployeeList/EmployeeBirthdaysPartial'
        page = 1

        while True:
            request_query_params = {'page': page}

            with bound_contextvars(request_query_params=request_query_params):

                log.debug('Fetching employee birthdays: sending request')
                response = self.__http_client.get(
                    url=url,
                    params=request_query_params,
                    cookies=cookies,
                )
                log.debug(
                    'Fetching employee birthdays: received response',
                    status=response.status_code,
                )

                is_end = yield response.text

            if is_end:
                break

            page += 1
