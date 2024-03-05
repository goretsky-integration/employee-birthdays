from collections.abc import Iterable

import httpx
import structlog.stdlib

from models import UnitEmployeeBirthdays

__all__ = ('BirthdayNotifier',)

log = structlog.stdlib.get_logger('app')


class BirthdayNotifier:

    def __init__(
            self,
            *,
            chat_id: int,
            unit_id_to_name: dict[int, str],
            bot_token: str,
    ):
        self.__chat_id = chat_id
        self.__unit_id_to_name = unit_id_to_name
        self.__bot_token = bot_token

    @property
    def base_url(self) -> str:
        return f'https://api.telegram.org/bot{self.__bot_token}'

    def _format_message(
            self,
            *,
            unit_id: int,
            employee_full_name: str,
    ) -> str:
        unit_name = self.__unit_id_to_name[unit_id]
        return (
            f'Банда, сегодня свой день рождения празднует'
            f' {employee_full_name} из пиццерии {unit_name} 🎇🎇🎇\n'
            'Поздравляем тебя и желаем всего самого наилучшего 🥳'
        )

    def _send_notification(
            self,
            *,
            http_client: httpx.Client,
            unit_id: int,
            employee_full_name: str,
    ):
        response = http_client.post('/sendMessage', json={
            'chat_id': self.__chat_id,
            'text': self._format_message(
                unit_id=unit_id,
                employee_full_name=employee_full_name,
            ),
        })

        if response.is_error:
            log.error(
                'Failed to send a message to the'
                ' Goretsky Band channel',
                response=response.text,
            )
        else:
            log.info('Sent a message to the Goretsky Band channel')

    def send_notifications(
            self,
            units_employee_birthdays: Iterable[UnitEmployeeBirthdays],
    ):
        with httpx.Client(base_url=self.base_url) as http_client:
            for unit_employee_birthday in units_employee_birthdays:
                for employee_birthday in unit_employee_birthday.employee_birthdays:
                    self._send_notification(
                        http_client=http_client,
                        unit_id=unit_employee_birthday.unit_id,
                        employee_full_name=employee_birthday.full_name,
                    )
