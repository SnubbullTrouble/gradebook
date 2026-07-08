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
class ClassAssignmentDTO:
    id: int
    class_id: int
    assignment_id: int
    total_points: float


@dataclass
class AssignmentCategoryWeightDTO:
    id: int
    class_id: int
    category: str
    weight: float


@dataclass
class StudentAssignmentScoreDTO:
    id: int
    roster_entry_id: int
    class_assignment_id: int
    total_score: float
    total_time: int | None


@dataclass
class StudentQuestionScoreDTO:
    id: int
    student_id: int
    assignment_question_id: int
    points_scored: float


@dataclass
class AssignmentDTO:
    id: int
    title: str
    category: str
    questions: list[AssignmentQuestionDTO]
