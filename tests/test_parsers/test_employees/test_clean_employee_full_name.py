import pytest

from parsers.employees import clean_employee_full_name


@pytest.mark.parametrize(
    'actual_name, expected_name',
    [
        ('СЗ Иванов Иван', 'Иванов Иван'),
        ('У Петров Петр', 'Петров Петр'),
        ('К Сидоров Сидор', 'Сидоров Сидор'),
        ('Сидоров Сидор', 'Сидоров Сидор'),
        ('СЗидоров Сидор', 'СЗидоров Сидор'),
        ('Уидоров Сидор', 'Уидоров Сидор'),
        ('Кидоров Сидор', 'Кидоров Сидор'),
    ]
)
def test_clean_employee_full_name(actual_name, expected_name):
    assert clean_employee_full_name(actual_name) == expected_name


def test_clean_employee_full_name_empty():
    assert clean_employee_full_name('') == ''
