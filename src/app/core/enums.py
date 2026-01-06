from enum import Enum


class history_status(Enum):
    upcoming = "upcoming"
    finished = "finished"
    cancelled = "cancelled"
    not_started = "not_started"


class attendance_status(Enum):
    present = "present"
    absent = "absent"
    late = "late"
    not_happened = "not_happened"
    unknown = "unknown"
