from collections import defaultdict

import httpx
from pydantic import TypeAdapter

from models import Unit

__all__ = ('get_units', 'group_unit_ids_by_account_name')


def get_units(base_url: str) -> list[Unit]:
    with httpx.Client(base_url=base_url) as http_client:
        response = http_client.get('/units/')

    response_data = response.json()

    type_adapter = TypeAdapter(list[Unit])
    return type_adapter.validate_python(response_data['units'])


def group_unit_ids_by_account_name(units: list[Unit]) -> dict[str, set[int]]:
    account_name_to_unit_ids: defaultdict[str, set[int]] = defaultdict(set)

    for unit in units:
        account_name_to_unit_ids[unit.dodo_is_api_account_name].add(unit.id)

    return dict(account_name_to_unit_ids)
