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
    ) -> Generator[HTML, bool, None]:
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

                yield HTML(response.text)

            page += 1

    def search_employees(self, name: str, cookies: dict[str, str]) -> HTML:
        url = '/OfficeManager/EmployeeList/StaffListPartial'

        request_data = {'employeeName': name}

        with bound_contextvars(request_data=request_data):
            log.debug('Searching employees: sending request')
            response = self.__http_client.post(
                url=url,
                data=request_data,
                cookies=cookies,
            )
            log.debug(
                'Searching employees: received response',
                status=response.status_code,
            )

            return HTML(response.text)
