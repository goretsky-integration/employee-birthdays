import contextlib
from collections.abc import Generator

import httpx

from new_types import (
    AuthCredentialsStorageConnectionHttpClient,
    DodoIsApiHttpClient,
)

__all__ = (
    "closing_dodo_is_api_http_client",
    "closing_auth_credentials_storage_connection_http_client",
)


@contextlib.contextmanager
def closing_dodo_is_api_http_client(
    base_url,
    **kwargs,
) -> Generator[DodoIsApiHttpClient, None, None]:
    with httpx.Client(timeout=30, base_url=base_url, **kwargs) as http_client:
        yield DodoIsApiHttpClient(http_client)


@contextlib.contextmanager
def closing_auth_credentials_storage_connection_http_client(
    base_url: str,
    **kwargs,
) -> Generator[AuthCredentialsStorageConnectionHttpClient, None, None]:
    with httpx.Client(timeout=30, base_url=base_url, **kwargs) as http_client:
        yield AuthCredentialsStorageConnectionHttpClient(http_client)
