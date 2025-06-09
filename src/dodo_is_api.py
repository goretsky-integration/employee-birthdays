from collections.abc import Iterable
from dataclasses import dataclass
from uuid import UUID

from pydantic import TypeAdapter

from models.employee_birthdays import StaffMemberBirthdayItem
from new_types.http_clients import DodoIsApiHttpClient


@dataclass(frozen=True, slots=True, kw_only=True)
class DodoIsApiGateway:
    http_client: DodoIsApiHttpClient
    access_token: str

    def get_employee_birthdays(
        self,
        *,
        day_from: int,
        day_to: int,
        month_from: int,
        month_to: int,
        unit_ids: Iterable[UUID],
    ) -> list[StaffMemberBirthdayItem]:
        url = "/staff/members/birthdays"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
        request_data = {
            "dayFrom": day_from,
            "dayTo": day_to,
            "monthFrom": month_from,
            "monthTo": month_to,
            "units": ",".join(unit_id.hex for unit_id in unit_ids),
            "take": 100,
            "skip": 0,
        }

        type_adapter = TypeAdapter(list[StaffMemberBirthdayItem])

        result: list[StaffMemberBirthdayItem] = []
        max_pages = 10
        for _ in range(max_pages):
            response = self.http_client.get(url, params=request_data, headers=headers)
            response_data = response.json()

            result += type_adapter.validate_python(response_data["birthdays"])
            if response_data["isEndOfListReached"]:
                break

            request_data["skip"] += request_data["take"]

        return result
