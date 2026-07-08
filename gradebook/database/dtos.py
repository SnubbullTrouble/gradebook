from dataclasses import dataclass


@dataclass
class StudentDTO:
    id: int
    student_number: str
    first_name: str
    last_name: str
