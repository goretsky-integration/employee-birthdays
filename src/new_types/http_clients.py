from typing import NewType

import httpx

__all__ = ('DodoISConnectionHttpClient',)

DodoISConnectionHttpClient = NewType('DodoISConnectionHttpClient', httpx.Client)
