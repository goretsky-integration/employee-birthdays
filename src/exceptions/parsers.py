import httpx

from pydantic import BaseModel, TypeAdapter

__all__ = ('HttpResponseJsonParseError', 'ResponseDataParseError')


class HttpResponseJsonParseError(Exception):

    def __init__(self, response: httpx.Response):
        super().__init__()
        self.response = response


class ResponseDataParseError(Exception):

    def __init__(
            self,
            *,
            response_data: dict | list,
            type_to_parse: type[BaseModel] | TypeAdapter,
    ):
        super().__init__()
        self.response_data = response_data
        self.type_to_parse = type_to_parse

    def __str__(self):
        return (
            f'Failed to parse {self.response_data} to {self.type_to_parse}'
        )
