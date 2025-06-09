import datetime
from typing import Annotated

from pydantic import BaseModel, Field


__all__ = ("StaffMemberBirthdayItem",)


class StaffMemberBirthdayItem(BaseModel):
    first_name: Annotated[str, Field(validation_alias="firstName")]
    last_name: Annotated[str, Field(validation_alias="lastName")]
    date_of_birth: Annotated[datetime.date, Field(validation_alias="dateOfBirth")]
    unit_name: Annotated[str, Field(validation_alias="unitName")]

    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name}"
