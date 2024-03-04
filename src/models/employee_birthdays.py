from pydantic import BaseModel

__all__ = ('EmployeeBirthday', 'UnitEmployeeBirthdays')


class EmployeeBirthday(BaseModel):
    full_name: str
    position: str
    age: str


class UnitEmployeeBirthdays(BaseModel):
    unit_id: int
    employee_birthdays: list[EmployeeBirthday]
