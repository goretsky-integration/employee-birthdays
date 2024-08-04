from context.employee_birthdays import filter_employee_birthdays_by_full_name
from models import EmployeeBirthday


def test_filter_employee_birthdays_by_substring():
    employee_birthdays = (
        EmployeeBirthday(
            unit_id=1,
            full_name="John Doe",
            position="Pizzamaker",
            age="25",
        ),
    )

    actual = filter_employee_birthdays_by_full_name(
        employee_birthdays=employee_birthdays,
        employees_blacklist=['john']
    )

    assert actual == []


def test_filter_employee_birthdays_by_full_name():
    employee_birthdays = (
        EmployeeBirthday(
            unit_id=1,
            full_name="John Doe",
            position="Pizzamaker",
            age="25",
        ),
    )

    actual = filter_employee_birthdays_by_full_name(
        employee_birthdays=employee_birthdays,
        employees_blacklist=['John Doe']
    )

    assert actual == []
