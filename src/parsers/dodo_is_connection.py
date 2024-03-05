from bs4 import BeautifulSoup

from exceptions import EmployeeBirthdaysParseError
from models import EmployeeBirthday
from new_types import HTML
from parsers.employees import clean_employee_full_name

__all__ = ('parse_employee_birthdays_html',)


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

        full_name = clean_employee_full_name(full_name.text)
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
