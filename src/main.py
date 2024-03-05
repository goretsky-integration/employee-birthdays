import pathlib

import structlog.stdlib

from config import load_config_from_file
from context.accounts import (
    get_accounts,
    iter_accounts_cookies,
    to_account_names,
)
from context.employee_birthdays import (
    filter_units_birthdays_by_employees,
    get_employee_birthdays,
)
from context.events import EventSerializer
from context.units import get_units, group_unit_ids_by_account_name
from dodo_is_connection import DodoISConnection
from enums import CountryCode
from http_clients import (
    closing_auth_credentials_storage_connection_http_client,
    closing_dodo_is_connection_http_client,
)
from message_queue import get_message_queue_channel, send_events
from models import Event, UnitEmployeeBirthdays
from telegram import BirthdayNotifier

log = structlog.stdlib.get_logger('app')


def main():
    config_file_path = pathlib.Path(__file__).parent.parent / 'config.toml'
    config = load_config_from_file(config_file_path)

    units = get_units(base_url=str(config.units_storage_base_url))

    account_name_to_unit_ids = group_unit_ids_by_account_name(units)

    serializer = EventSerializer(
        unit_id_to_name={unit.id: unit.name for unit in units},
    )

    birthday_notifier = BirthdayNotifier(
        bot_token=config.bot_token.get_secret_value(),
        chat_id=config.goretsky_band_chat_id,
        unit_id_to_name={unit.id: unit.name for unit in units},
    )

    units_employee_birthdays: list[UnitEmployeeBirthdays] = []

    with (
        closing_auth_credentials_storage_connection_http_client(
            base_url=str(config.auth_credentials_storage_base_url),
        )
        as auth_credentials_storage_connection_http_client,

        closing_dodo_is_connection_http_client(country_code=CountryCode.RU)
        as dodo_is_connection_http_client
    ):
        office_manager_accounts = get_accounts(
            http_client=auth_credentials_storage_connection_http_client,
        )

        accounts_cookies_iterator = iter_accounts_cookies(
            http_client=auth_credentials_storage_connection_http_client,
            account_names=to_account_names(office_manager_accounts),
        )

        for account_cookies in accounts_cookies_iterator:
            dodo_is_connection = DodoISConnection(
                http_client=dodo_is_connection_http_client,
                cookies=account_cookies.cookies,
            )
            units_employee_birthdays += get_employee_birthdays(
                dodo_is_connection=dodo_is_connection,
                unit_ids=account_name_to_unit_ids[account_cookies.account_name],
            )

    units_employee_birthdays = filter_units_birthdays_by_employees(
        units_employee_birthdays=units_employee_birthdays,
        employees_blacklist=config.employees_blacklist,
    )

    events: list[Event] = []

    for unit_employee_birthdays in units_employee_birthdays:
        events += serializer.serialize(unit_employee_birthdays)

    try:
        with get_message_queue_channel(
                rabbitmq_url=str(config.message_queue_url),
        ) as message_queue_channel:
            send_events(channel=message_queue_channel, events=events)
    except Exception:
        log.exception('Failed to send events to the message queue')

    try:
        birthday_notifier.send_notifications(units_employee_birthdays)
    except Exception:
        log.exception(
            'Failed to send birthday notifications to the Goretsky Band channel'
        )


if __name__ == '__main__':
    main()
