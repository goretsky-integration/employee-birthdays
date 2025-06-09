from collections.abc import Iterable

from auth_credentials_storage import AuthCredentialsStorageConnection
from models import Account, AccountAccessToken
from new_types import AuthCredentialsStorageConnectionHttpClient
from parsers import (
    filter_api_accounts,
    parse_accounts_response,
)
from parsers.account_cookies import parse_access_token_response
from models.units import Unit

__all__ = ("get_accounts", "get_account_access_tokens", "to_account_names")


def get_accounts(
    http_client: AuthCredentialsStorageConnectionHttpClient,
) -> list[Account]:
    """Get all accounts from the auth credentials storage."""
    connection = AuthCredentialsStorageConnection(http_client)
    accounts_response = connection.get_accounts()
    accounts = parse_accounts_response(accounts_response)
    return filter_api_accounts(accounts)


def get_account_access_tokens(
    account_names: Iterable[str],
    http_client: AuthCredentialsStorageConnectionHttpClient,
) -> list[AccountAccessToken]:
    """Get cookies for the specified accounts."""
    connection = AuthCredentialsStorageConnection(http_client)
    result = []
    for account_name in account_names:
        response = connection.get_access_token(account_name)
        result.append(parse_access_token_response(response))
    return result


def to_account_names(units: Iterable[Unit]) -> set[str]:
    """Get account names from the accounts."""
    return {unit.dodo_is_api_account_name for unit in units}
