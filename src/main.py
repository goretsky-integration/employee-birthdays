import itertools
import pathlib
import datetime

from config import load_config_from_file
from context.accounts import (
    get_account_access_tokens,
    to_account_names,
)
from context.employee_birthdays import filter_employee_birthdays_by_full_name
from context.units import get_units
from http_clients import (
    closing_auth_credentials_storage_connection_http_client,
    closing_dodo_is_api_http_client,
)
from logger import create_logger
from models import StaffMemberBirthdayItem
from dodo_is_api import DodoIsApiGateway
from telegram import TelegramBotApiConnection
from views import render_congratulations

logger = create_logger("app")


def main():
    config_file_path = pathlib.Path(__file__).parent.parent / "config.toml"
    config = load_config_from_file(config_file_path)
    
    now = datetime.datetime.now(config.timezone)

    telegram_bot_api_connection = TelegramBotApiConnection(
        token=config.bot_token.get_secret_value(),
    )

    units = get_units(base_url=str(config.units_storage_base_url))
    
    employee_birthdays: list[StaffMemberBirthdayItem] = []

    with (
        closing_auth_credentials_storage_connection_http_client(
            base_url=str(config.auth_credentials_storage_base_url),
        ) as auth_credentials_storage_connection_http_client,
        closing_dodo_is_api_http_client(
            base_url=config.base_url
        ) as dodo_is_connection_http_client,
    ):
        accounts_access_tokens = get_account_access_tokens(
            http_client=auth_credentials_storage_connection_http_client,
            account_names=to_account_names(units),
        )

        for account_access_token in accounts_access_tokens:
            dodo_is_api_gateway = DodoIsApiGateway(
                http_client=dodo_is_connection_http_client,
                access_token=account_access_token.access_token,
            )
            for units_batch in itertools.batched(units, n=30):
                unit_ids = [unit.uuid for unit in units_batch]
                employee_birthdays += dodo_is_api_gateway.get_employee_birthdays(
                    day_from=now.day,
                    day_to=now.day,
                    month_from=now.month,
                    month_to=now.month,
                    unit_ids=unit_ids,
                )

    employee_birthdays = filter_employee_birthdays_by_full_name(
        employee_birthdays=employee_birthdays,
        employees_blacklist=config.employees_blacklist,
    )

    if not employee_birthdays:
        logger.info("No employee birthdays to congratulate")
        return

    congratulations_text = render_congratulations(employee_birthdays)

    telegram_bot_api_connection.send_message(
        chat_id=config.goretsky_band_chat_id,
        text=congratulations_text,
    )


if __name__ == "__main__":
    main()
