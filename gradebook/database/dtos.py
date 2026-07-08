from dataclasses import dataclass
from datetime import date


@dataclass
class StudentDTO:
    id: int
    student_number: str
    first_name: str
    last_name: str


@dataclass
class ClassDTO:
    id: int
    name: str
    start_date: date | None
    end_date: date | None


@dataclass
class AssignmentQuestionDTO:
    id: int
    assignment_id: int
    text: str
    point_value: int


@dataclass
class AssignmentDTO:
    id: int
    title: str
    category: str
    questions: list[AssignmentQuestionDTO]
