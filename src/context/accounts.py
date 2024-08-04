from collections.abc import Generator, Iterable

from auth_credentials_storage import AuthCredentialsStorageConnection
from models import Account, AccountCookies
from new_types import AuthCredentialsStorageConnectionHttpClient
from parsers import (
    filter_office_manager_accounts,
    parse_account_cookies_response,
    parse_accounts_response,
)

__all__ = ('get_accounts', 'iter_accounts_cookies', 'to_account_names')


def get_accounts(
        http_client: AuthCredentialsStorageConnectionHttpClient,
) -> list[Account]:
    """Get all accounts from the auth credentials storage."""
    connection = AuthCredentialsStorageConnection(http_client)
    accounts_response = connection.get_accounts()
    accounts = parse_accounts_response(accounts_response)
    return filter_office_manager_accounts(accounts)


def iter_accounts_cookies(
        account_names: Iterable[str],
        http_client: AuthCredentialsStorageConnectionHttpClient,
) -> Generator[AccountCookies, None, None]:
    """Get cookies for the specified accounts."""
    connection = AuthCredentialsStorageConnection(http_client)
    for account_name in account_names:
        account_cookies_response = connection.get_cookies(account_name)
        yield parse_account_cookies_response(account_cookies_response)


def to_account_names(accounts: Iterable[Account]) -> set[str]:
    """Get account names from the accounts."""
    return {account.name for account in accounts}
