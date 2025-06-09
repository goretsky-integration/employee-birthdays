import httpx
from pydantic import ValidationError

from exceptions import ResponseDataParseError
from models import AccountAccessToken
from parsers.http_responses import try_parse_response_json

__all__ = ("parse_access_token_response",)


def parse_access_token_response(response: httpx.Response) -> AccountAccessToken:
    response_data = try_parse_response_json(response)

    try:
        return AccountAccessToken.model_validate(response_data)
    except ValidationError as error:
        raise ResponseDataParseError(
            response_data=response_data,
            type_to_parse=AccountAccessToken,
        ) from error
