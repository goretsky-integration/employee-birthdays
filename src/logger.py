import json
import logging.config
import pathlib
from typing import Any, Final

__all__ = (
    'CONFIG_FILE_PATH',
    'load_config_from_file',
    'create_logger',
)

CONFIG_FILE_PATH: Final[pathlib.Path] = (
        pathlib.Path(__file__).parent.parent / 'logging_config.json'
)


def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.propagate = False
    return logger


def load_config_from_file(
        config_file_path: pathlib.Path = CONFIG_FILE_PATH,
) -> dict[str, Any]:
    config_json = config_file_path.read_text(encoding='utf-8')
    return json.loads(config_json)


def setup_logging(
        config_file_path: pathlib.Path = CONFIG_FILE_PATH,
):
    config = load_config_from_file(config_file_path)
    logging.config.dictConfig(config)
