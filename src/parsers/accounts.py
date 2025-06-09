from collections.abc import Iterable

import httpx
from pydantic import TypeAdapter, ValidationError

from exceptions import ResponseDataParseError
from models import Account
from parsers.http_responses import try_parse_response_json

__all__ = ('parse_accounts_response', 'filter_api_accounts')


def parse_accounts_response(response: httpx.Response) -> tuple[Account, ...]:
    type_adapter = TypeAdapter(tuple[Account, ...])
    response_data = try_parse_response_json(response)

    try:
        return type_adapter.validate_python(response_data)
    except ValidationError as error:
        raise ResponseDataParseError(
            response_data=response_data,
            type_to_parse=type_adapter
        ) from error


def filter_api_accounts(
        accounts: Iterable[Account],
) -> list[Account]:
    return [
        account
        for account in accounts
        if account.name.startswith('api')
    ]
