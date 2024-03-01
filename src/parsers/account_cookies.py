import httpx
from pydantic import ValidationError

from exceptions import ResponseDataParseError
from models import AccountCookies
from parsers.http_responses import try_parse_response_json

__all__ = ('parse_account_cookies_response',)


def parse_account_cookies_response(response: httpx.Response) -> AccountCookies:
    response_data = try_parse_response_json(response)

    try:
        return AccountCookies.model_validate(response_data)
    except ValidationError:
        raise ResponseDataParseError(
            response_data=response_data,
            type_to_parse=AccountCookies,
        )
