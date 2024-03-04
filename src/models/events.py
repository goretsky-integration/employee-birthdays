from typing import TypedDict

__all__ = ('Event', 'EventPayload')


class EventPayload(TypedDict):
    unit_name: str
    employee_full_name: str


class Event(TypedDict):
    unit_id: int
    type: str
    payload: EventPayload
