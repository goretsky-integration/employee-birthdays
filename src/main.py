import pathlib

import structlog.stdlib

from config import load_config_from_file
from context.accounts import (
    get_accounts,
    iter_accounts_cookies,
    to_account_names,
)
from context.employee_birthdays import (
    filter_employee_birthdays_in_blacklist,
    get_employee_birthdays,
)
from context.units import get_units, group_unit_ids_by_account_name
from dodo_is_connection import DodoISConnection
from enums import CountryCode
from http_clients import (
    closing_auth_credentials_storage_connection_http_client,
    closing_dodo_is_connection_http_client,
)
from models import EmployeeBirthday
from telegram import TelegramBotApiConnection
from views import render_congratulations

log = structlog.stdlib.get_logger('app')


def main():
    config_file_path = pathlib.Path(__file__).parent.parent / 'config.toml'
    config = load_config_from_file(config_file_path)

    telegram_bot_api_connection = TelegramBotApiConnection(
        token=config.bot_token.get_secret_value(),
    )

    units = get_units(base_url=str(config.units_storage_base_url))

    account_name_to_unit_ids = group_unit_ids_by_account_name(units)

    employee_birthdays: list[EmployeeBirthday] = []

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
            employee_birthdays += get_employee_birthdays(
                dodo_is_connection=dodo_is_connection,
                unit_ids=account_name_to_unit_ids[account_cookies.account_name],
            )

    employee_birthdays = filter_employee_birthdays_in_blacklist(
        employee_birthdays=employee_birthdays,
        employees_blacklist=config.employees_blacklist,
    )

    if not employee_birthdays:
        log.info('No employee birthdays to congratulate')
        return

    congratulations_text = render_congratulations(
        employee_birthdays=employee_birthdays,
        unit_id_to_name={unit.id: unit.name for unit in units},
    )
    telegram_bot_api_connection.send_message(
        chat_id=config.goretsky_band_chat_id,
        text=congratulations_text,
    )


if __name__ == '__main__':
    main()
