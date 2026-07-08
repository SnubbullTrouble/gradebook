from peewee import prefetch
from .models import (
    Assignment,
    AssignmentQuestion,
    Class,
    ClassAssignment,
)
from .models import Student
from .dtos import StudentDTO


def create_student_dto(student_number: str, first_name: str, last_name: str) -> StudentDTO:
    s = Student.create(student_number=student_number, first_name=first_name, last_name=last_name)
    return StudentDTO(id=s.id, student_number=s.student_number, first_name=s.first_name, last_name=s.last_name)


def get_student_by_number_dto(student_number: str) -> StudentDTO | None:
    s = Student.get_or_none(Student.student_number == student_number)
    if s is None:
        return None
    return StudentDTO(id=s.id, student_number=s.student_number, first_name=s.first_name, last_name=s.last_name)


def get_class_by_id(class_id: int):
    """Return Class or None for the given id."""
    return Class.get_or_none(Class.id == class_id)


def fetch_assignments_for_class(class_id: int, category: str | None = None):
    base_q = (
        Assignment.select()
        .join(ClassAssignment)
        .join(Class)
        .where(Class.id == class_id)
    )
    if category:
        base_q = base_q.where(Assignment.category == category)

    return list(prefetch(base_q, AssignmentQuestion))
