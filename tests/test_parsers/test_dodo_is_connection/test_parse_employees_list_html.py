import pathlib

import pytest

from exceptions import EmployeesListParseError
from new_types import HTML
from parsers.dodo_is_connection import parse_employees_list_html



@pytest.fixture
def single_employee_list_html() -> HTML:
    file_path = (
            pathlib.Path(__file__).parent
            / './employees_lists/single_employee.html'
    )
    with open(file_path, encoding='utf-8') as file:
        return HTML(file.read())


@pytest.fixture
def multiple_employees_list_html() -> HTML:
    file_path = (
            pathlib.Path(__file__).parent
            / './employees_lists/multiple_employees.html'
    )
    with open(file_path, encoding='utf-8') as file:
        return HTML(file.read())


@pytest.fixture
def no_employees_list_html() -> HTML:
    file_path = (
            pathlib.Path(__file__).parent
            / './employees_lists/no_employees.html'
    )
    with open(file_path, encoding='utf-8') as file:
        return HTML(file.read())


@pytest.fixture
def no_a_tag_html() -> HTML:
    file_path = (
            pathlib.Path(__file__).parent
            / './employees_lists/no_a_tag.html'
    )
    with open(file_path, encoding='utf-8') as file:
        return HTML(file.read())


@pytest.fixture
def no_href_in_a_tag_html() -> HTML:
    file_path = (
            pathlib.Path(__file__).parent
            / './employees_lists/no_href_in_a_tag.html'
    )
    with open(file_path, encoding='utf-8') as file:
        return HTML(file.read())


@pytest.fixture
def invalid_employee_id_html() -> HTML:
    file_path = (
            pathlib.Path(__file__).parent
            / './employees_lists/invalid_employee_id.html'
    )
    with open(file_path, encoding='utf-8') as file:
        return HTML(file.read())


def test_parse_single_employee_html(single_employee_list_html: HTML):
    employee_ids = parse_employees_list_html(single_employee_list_html)
    assert employee_ids == {202992}


def test_parse_multiple_employees_html(multiple_employees_list_html: HTML):
    employee_ids = parse_employees_list_html(multiple_employees_list_html)
    assert employee_ids == {202992, 158234}


def test_parse_empty_employees_html(no_employees_list_html: HTML):
    employee_ids = parse_employees_list_html(no_employees_list_html)
    assert employee_ids == set()


def test_no_table_html():
    with pytest.raises(EmployeesListParseError) as error:
        parse_employees_list_html(HTML(''))

    assert error.value.args[0] == 'Failed to find table with employees list'
    assert error.value.html == HTML('')


def test_no_a_tag_html(no_a_tag_html: HTML):
    with pytest.raises(EmployeesListParseError) as error:
        parse_employees_list_html(no_a_tag_html)

    assert error.value.args[0] == 'Failed to find employee page url'
    assert error.value.html == no_a_tag_html


def test_no_href_in_a_tag(no_href_in_a_tag_html: HTML):
    with pytest.raises(EmployeesListParseError) as error:
        parse_employees_list_html(no_href_in_a_tag_html)

    assert error.value.args[0] == 'Failed to find employee page url'
    assert error.value.html == no_href_in_a_tag_html


def test_invalid_employee_id(invalid_employee_id_html: HTML):
    with pytest.raises(EmployeesListParseError) as error:
        parse_employees_list_html(invalid_employee_id_html)

    assert error.value.args[0] == 'Failed to parse employee id'
    assert error.value.html == invalid_employee_id_html
