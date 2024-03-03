from bs4 import BeautifulSoup

from exceptions import EmployeeBirthdaysParseError, EmployeesListParseError
from models import EmployeeBirthday
from new_types import EmployeeId, HTML

__all__ = (
    'parse_employee_birthdays_html',
    'parse_employees_list_html',
)


def parse_employee_birthdays_html(html: HTML) -> list[EmployeeBirthday]:
    soup = BeautifulSoup(html, 'lxml')

    table = soup.find('table')

    if table is None:
        raise EmployeeBirthdaysParseError(
            'Failed to find table with employee birthdays',
            html=html,
        )

    table_rows = table.find_all('tr')[1:]

    employee_birthdays: list[EmployeeBirthday] = []
    for table_row in table_rows:
        full_name, position, age = table_row.find_all('td')

        full_name = full_name.text
        position = position.text
        age = age.text

        if not all((full_name, position, age)):
            continue

        employee_birthdays.append(
            EmployeeBirthday(
                full_name=full_name,
                position=position,
                age=age,
            ),
        )

    return employee_birthdays


def parse_employees_list_html(html: HTML) -> set[EmployeeId]:
    """Parse employees list page and return set of employee ids."""
    soup = BeautifulSoup(html, 'lxml')

    table = soup.find('table')

    if table is None:
        raise EmployeesListParseError(
            'Failed to find table with employees list',
            html=html,
        )

    table_rows = table.find_all('tr')[1:]

    employee_ids: set[EmployeeId] = set()
    for table_row in table_rows:

        a_tag = table_row.find('a')

        if a_tag is None:
            raise EmployeesListParseError(
                'Failed to find employee page url',
                html=html,
            )

        try:
            employee_page_url = a_tag['href']
        except KeyError:
            raise EmployeesListParseError(
                'Failed to find employee page url',
                html=html,
            )

        try:
            employee_id = EmployeeId(int(employee_page_url.split('=')[-1]))
        except ValueError:
            raise EmployeesListParseError(
                'Failed to parse employee id',
                html=html,
            )

        employee_ids.add(employee_id)

    return employee_ids
