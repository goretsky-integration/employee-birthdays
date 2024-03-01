import json

import httpx

from exceptions import HttpResponseJsonParseError

__all__ = ('try_parse_response_json',)


def try_parse_response_json(response: httpx.Response) -> dict | list:
    try:
        return response.json()
    except json.JSONDecodeError:
        raise HttpResponseJsonParseError(response)
