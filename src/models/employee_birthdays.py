from pydantic import BaseModel

__all__ = ('EmployeeBirthday',)


class EmployeeBirthday(BaseModel):
    unit_id: int
    full_name: str
    position: str
    age: str
