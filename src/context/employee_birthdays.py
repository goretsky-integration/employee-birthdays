from collections.abc import Iterable

from models import StaffMemberBirthdayItem

__all__ = (
    'filter_employee_birthdays_by_full_name',
)


def filter_employee_birthdays_by_full_name(
        *,
        employee_birthdays: Iterable[StaffMemberBirthdayItem],
        employees_blacklist: Iterable[str],
) -> list[StaffMemberBirthdayItem]:
    employees_blacklist = {name.lower() for name in employees_blacklist}

    result: list[StaffMemberBirthdayItem] = []

    for employee_birthday in employee_birthdays:
        for employee_in_blacklist in employees_blacklist:
            if employee_in_blacklist in employee_birthday.full_name.lower():
                break
        else:
            result.append(employee_birthday)

    return result
