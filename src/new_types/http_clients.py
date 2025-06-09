from typing import NewType

import httpx

__all__ = (
    "AuthCredentialsStorageConnectionHttpClient",
    "DodoIsApiHttpClient",
)

AuthCredentialsStorageConnectionHttpClient = NewType(
    "AuthCredentialsStorageConnectionHttpClient", httpx.Client
)
DodoIsApiHttpClient = NewType("DodoIsApiHttpClient", httpx.Client)
