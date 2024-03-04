from collections.abc import Generator

import structlog.stdlib
from structlog.contextvars import bound_contextvars

from new_types import DodoISConnectionHttpClient, HTML

__all__ = ('DodoISConnection',)

log = structlog.stdlib.get_logger('app')


class DodoISConnection:

    def __init__(
            self,
            *,
            http_client: DodoISConnectionHttpClient,
            cookies: dict[str, str],
    ):
        self.__http_client = http_client
        self.__cookies = cookies

    def iter_employee_birthdays(
            self,
            unit_id: int,
    ) -> Generator[HTML, None, None]:
        url = '/OfficeManager/EmployeeList/EmployeeBirthdaysPartial'
        page = 1

        while True:
            request_query_params = {'page': page, 'unitId': unit_id}

            with bound_contextvars(request_query_params=request_query_params):
                log.debug('Fetching employee birthdays: sending request')
                response = self.__http_client.get(
                    url=url,
                    params=request_query_params,
                    cookies=self.__cookies,
                )
                log.debug(
                    'Fetching employee birthdays: received response',
                    status=response.status_code,
                )

                yield HTML(response.text)

            page += 1
