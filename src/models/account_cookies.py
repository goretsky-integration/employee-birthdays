from pydantic import BaseModel

__all__ = ("AccountAccessToken",)


class AccountAccessToken(BaseModel):
    access_token: str
    account_name: str
