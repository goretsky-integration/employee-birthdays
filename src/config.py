import pathlib
import tomllib
from zoneinfo import ZoneInfo

from pydantic import BaseModel, HttpUrl, SecretStr


__all__ = ('Config', 'load_config_from_file')


class Config(BaseModel):
    """Configuration of the application."""
    timezone: ZoneInfo
    auth_credentials_storage_base_url: HttpUrl
    units_storage_base_url: HttpUrl
    base_url: str
    employees_blacklist: set[str]
    bot_token: SecretStr
    goretsky_band_chat_id: int


def load_config_from_file(file_path: pathlib.Path) -> Config:
    """Load configuration from the specified TOML file."""
    config_text = file_path.read_text(encoding='utf-8')
    config = tomllib.loads(config_text)

    return Config(
        timezone=ZoneInfo(config['timezone']),
        auth_credentials_storage_base_url=(
            config['api']['auth_credentials_storage_base_url']
        ),
        units_storage_base_url=config['api']['units_storage_base_url'],
        base_url=config['api']['base_url'],
        employees_blacklist=config['employees']['blacklist'],
        bot_token=config['telegram']['bot_token'],
        goretsky_band_chat_id=config['telegram']['goretsky_band_chat_id'],
    )
