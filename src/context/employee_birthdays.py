from collections.abc import Iterable

from dodo_is_connection import DodoISConnection
from models import EmployeeBirthday, UnitEmployeeBirthdays
from parsers.dodo_is_connection import parse_employee_birthdays_html

__all__ = (
    'get_unit_employee_birthdays',
    'get_employee_birthdays',
    'filter_units_birthdays_by_employees',
    'filter_employee_birthdays',
)


def filter_employee_birthdays(
        *,
        employee_birthdays: Iterable[EmployeeBirthday],
        employees_blacklist: Iterable[str],
) -> list[EmployeeBirthday]:
    employees_blacklist = set(employees_blacklist)
    return [
        employee_birthday for employee_birthday in employee_birthdays
        if employee_birthday.full_name not in employees_blacklist
    ]


def filter_units_birthdays_by_employees(
        *,
        units_employee_birthdays: Iterable[UnitEmployeeBirthdays],
        employees_blacklist: Iterable[str],
) -> list[UnitEmployeeBirthdays]:
    employees_blacklist = set(employees_blacklist)

    return [
        UnitEmployeeBirthdays(
            unit_id=unit_employee_birthdays.unit_id,
            employee_birthdays=employee_birthdays,
        )
        for unit_employee_birthdays in units_employee_birthdays
        if (employee_birthdays := filter_employee_birthdays(
            employee_birthdays=unit_employee_birthdays.employee_birthdays,
            employees_blacklist=employees_blacklist,
        ))
    ]


def get_unit_employee_birthdays(
        *,
        dodo_is_connection: DodoISConnection,
        unit_id: int,
) -> list[EmployeeBirthday]:
    employee_birthdays_iterator = (
        dodo_is_connection.iter_employee_birthdays(unit_id=unit_id)
    )

    unit_employee_birthdays: list[EmployeeBirthday] = []
    for employee_birthdays_html in employee_birthdays_iterator:
        employee_birthdays = parse_employee_birthdays_html(
            html=employee_birthdays_html,
        )
        if not employee_birthdays:
            break

        unit_employee_birthdays += employee_birthdays

    return unit_employee_birthdays


def get_employee_birthdays(
        dodo_is_connection: DodoISConnection,
        unit_ids: Iterable[int],
) -> list[UnitEmployeeBirthdays]:
    units_employee_birthdays: list[UnitEmployeeBirthdays] = []

    for unit_id in unit_ids:
        unit_employee_birthdays = get_unit_employee_birthdays(
            dodo_is_connection=dodo_is_connection,
            unit_id=unit_id,
        )
        if unit_employee_birthdays:
            units_employee_birthdays.append(
                UnitEmployeeBirthdays(
                    unit_id=unit_id,
                    employee_birthdays=unit_employee_birthdays,
                ),
            )

    return units_employee_birthdays
