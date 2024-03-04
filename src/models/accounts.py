from pydantic import BaseModel

__all__ = ('Account',)


class Account(BaseModel):
    name: str
