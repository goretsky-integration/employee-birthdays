from collections.abc import Generator

from logger import create_logger
from new_types import DodoISConnectionHttpClient, HTML

__all__ = ('DodoISConnection',)

logger = create_logger('dodo_is_connection')


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

            logger.debug(
                'Fetching employee birthdays: sending request',
                extra={'params': request_query_params}
            )
            response = self.__http_client.get(
                url=url,
                params=request_query_params,
                cookies=self.__cookies,
            )
            logger.debug(
                'Fetching employee birthdays: received response',
                extra={
                    'response': response.text,
                    'status': response.status_code,
                },
            )

            yield HTML(response.text)

            page += 1
