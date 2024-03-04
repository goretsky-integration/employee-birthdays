from models import UnitEmployeeBirthdays

__all__ = ('EventSerializer',)


class EventSerializer:

    def __init__(self, unit_id_to_name: dict[int, str]):
        self.unit_id_to_name = unit_id_to_name

    def serialize(
            self,
            unit_employee_birthdays: UnitEmployeeBirthdays,
    ) -> list[dict]:
        unit_name = self.unit_id_to_name[unit_employee_birthdays.unit_id]
        return [
            {
                'unit_id': unit_employee_birthdays.unit_id,
                'type': 'EMPLOYEE_BIRTHDAY',
                'payload': {
                    'unit_name': unit_name,
                    'employee_full_name': employee_birthday.full_name,
                },
            }
            for employee_birthday in unit_employee_birthdays.employee_birthdays
        ]
