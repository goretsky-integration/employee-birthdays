import pytest

from exceptions import EmployeeBirthdaysParseError
from models import EmployeeBirthday
from new_types import HTML
from parsers.dodo_is_connection import parse_employee_birthdays_html


def test_parse_single_employee_birthday_html():
    html = HTML('''
    <div class="block-wrapper">
        <table class="b-table">
            <tr class="b-table__row b-table__row_head">
                <td class="b-table__col b-table__col_head">ФИО</td>
                <td class="b-table__col b-table__col_head">Тип</td>
                <td class="b-table__col b-table__col_head">Возраст</td>
            </tr>
            <tr class="b-table__row">
                <td class="b-table__col">Волошин Павел</td>
                <td class="b-table__col">Работник кухни</td>
                <td class="b-table__col">36 лет</td>
            </tr>
        </table>
    </div>
    <script type="text/javascript">
            $("#employeeBirthdaysCount").text('(1)');
    </script>
    ''')
    actual = parse_employee_birthdays_html(html)
    expected = [
        EmployeeBirthday(
            full_name='Волошин Павел',
            position='Работник кухни',
            age='36 лет',
        ),
    ]
    assert actual == expected


def test_parse_multiple_employee_birthdays_html():
    html = HTML('''
    <div class="block-wrapper">
        <table class="b-table">
            <tr class="b-table__row b-table__row_head">
                <td class="b-table__col b-table__col_head">ФИО</td>
                <td class="b-table__col b-table__col_head">Тип</td>
                <td class="b-table__col b-table__col_head">Возраст</td>
            </tr>
            <tr class="b-table__row">
                <td class="b-table__col">Волошин Павел</td>
                <td class="b-table__col">Работник кухни</td>
                <td class="b-table__col">36 лет</td>
            </tr>
            <tr class="b-table__row">
                <td class="b-table__col">Иванов Иван</td>
                <td class="b-table__col">Менеджер</td>
                <td class="b-table__col">40 лет</td>
            </tr>
        </table>
    </div>
    <script type="text/javascript">
            $("#employeeBirthdaysCount").text('(2)');
    </script>
    ''')
    actual = parse_employee_birthdays_html(html)
    expected = [
        EmployeeBirthday(
            full_name='Волошин Павел',
            position='Работник кухни',
            age='36 лет',
        ),
        EmployeeBirthday(
            full_name='Иванов Иван',
            position='Менеджер',
            age='40 лет',
        ),
    ]
    assert actual == expected


def test_parse_no_employee_birthdays_html():
    html = HTML('''
    <div class="block-wrapper">
        <table class="b-table">
            <tr class="b-table__row b-table__row_head">
                <td class="b-table__col b-table__col_head">ФИО</td>
                <td class="b-table__col b-table__col_head">Тип</td>
                <td class="b-table__col b-table__col_head">Возраст</td>
            </tr>
        </table>
    </div>
    <script type="text/javascript">
            $("#employeeBirthdaysCount").text('(0)');
    </script>
    ''')
    actual = parse_employee_birthdays_html(html)
    expected = []
    assert actual == expected


def test_parse_employee_birthdays_html_with_empty_table_data():
    html = HTML('''
    <div class="block-wrapper">
        <table class="b-table">
            <tr class="b-table__row b-table__row_head">
                <td class="b-table__col b-table__col_head">ФИО</td>
                <td class="b-table__col b-table__col_head">Тип</td>
                <td class="b-table__col b-table__col_head">Возраст</td>
            </tr>
            <tr class="b-table__row">
                <td class="b-table__col"></td>
                <td class="b-table__col"></td>
                <td class="b-table__col"></td>
            </tr>
        </table>
    </div>
    <script type="text/javascript">
            $("#employeeBirthdaysCount").text('(0)');
    </script>
    ''')
    actual = parse_employee_birthdays_html(html)
    expected = []
    assert actual == expected


def test_parse_employee_birthdays_html_with_empty_table():
    html = HTML('''
    <div class="block-wrapper">
        <table class="b-table">
        </table>
    </div>
    <script type="text/javascript">
            $("#employeeBirthdaysCount").text('(0)');
    </script>
    ''')
    actual = parse_employee_birthdays_html(html)
    expected = []
    assert actual == expected


def test_parse_employee_birthdays_html_with_no_table():
    html = HTML('''
    <div class="block-wrapper">
    </div>
    <script type="text/javascript">
            $("#employeeBirthdaysCount").text('(0)');
    </script>
    ''')
    with pytest.raises(EmployeeBirthdaysParseError) as error:
        parse_employee_birthdays_html(html)

    assert error.value.args[0] == 'Failed to find table with employee birthdays'
    assert error.value.html == html
