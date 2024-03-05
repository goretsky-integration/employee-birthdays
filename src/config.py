import pathlib
import tomllib

from pydantic import BaseModel, HttpUrl, AnyUrl, SecretStr

from enums.country_codes import CountryCode

__all__ = ('Config', 'load_config_from_file')


class Config(BaseModel):
    auth_credentials_storage_base_url: HttpUrl
    units_storage_base_url: HttpUrl
    country_code: CountryCode
    employees_blacklist: set[str]
    message_queue_url: AnyUrl
    bot_token: SecretStr
    goretsky_band_chat_id: int


def load_config_from_file(file_path: pathlib.Path) -> Config:
    config_text = file_path.read_text(encoding='utf-8')
    config = tomllib.loads(config_text)

    return Config(
        auth_credentials_storage_base_url=(
            config['api']['auth_credentials_storage_base_url']
        ),
        units_storage_base_url=config['api']['units_storage_base_url'],
        country_code=CountryCode(config['country_code']),
        employees_blacklist=config['employees']['blacklist'],
        message_queue_url=config['message_queue']['url'],
        bot_token=config['telegram']['bot_token'],
        goretsky_band_chat_id=config['telegram']['goretsky_band_chat_id'],
    )
