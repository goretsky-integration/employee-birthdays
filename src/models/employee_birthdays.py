from pydantic import BaseModel

__all__ = ('EmployeeBirthday',)


class EmployeeBirthday(BaseModel):
    full_name: str
    position: str
    age: str
