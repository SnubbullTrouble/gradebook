from peewee import prefetch
from .models import (
    Assignment,
    AssignmentQuestion,
    Class,
    ClassAssignment,
    Student,
)
from .dtos import (
    StudentDTO,
    AssignmentDTO,
    AssignmentQuestionDTO,
    ClassDTO,
)


def create_student_dto(student_number: str, first_name: str, last_name: str) -> StudentDTO:
    s = Student.create(student_number=student_number, first_name=first_name, last_name=last_name)
    return StudentDTO(id=s.id, student_number=s.student_number, first_name=s.first_name, last_name=s.last_name)


def get_student_by_number_dto(student_number: str) -> StudentDTO | None:
    s = Student.get_or_none(Student.student_number == student_number)
    if s is None:
        return None
    return StudentDTO(id=s.id, student_number=s.student_number, first_name=s.first_name, last_name=s.last_name)


def get_class_dto(class_id: int) -> ClassDTO | None:
    cls = Class.get_or_none(Class.id == class_id)
    if cls is None:
        return None
    return ClassDTO(
        id=cls.id,
        name=cls.name,
        start_date=cls.start_date,
        end_date=cls.end_date,
    )


def get_class_by_id(class_id: int) -> Class | None:
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


def get_assignment_question_dto(question_id: int) -> AssignmentQuestionDTO | None:
    q = AssignmentQuestion.get_or_none(AssignmentQuestion.id == question_id)
    if q is None:
        return None
    return AssignmentQuestionDTO(
        id=q.id,
        assignment_id=q.assignment.id,
        text=q.text,
        point_value=q.point_value,
    )


def get_questions_for_assignment_dto(assignment_id: int) -> list[AssignmentQuestionDTO]:
    questions = AssignmentQuestion.select().where(AssignmentQuestion.assignment == assignment_id)
    return [
        AssignmentQuestionDTO(
            id=q.id,
            assignment_id=q.assignment.id,
            text=q.text,
            point_value=q.point_value,
        )
        for q in questions
    ]


def get_assignment_dto(assignment_id: int) -> AssignmentDTO | None:
    assignment = Assignment.get_or_none(Assignment.id == assignment_id)
    if assignment is None:
        return None
    questions = get_questions_for_assignment_dto(assignment_id)
    return AssignmentDTO(
        id=assignment.id,
        title=assignment.title,
        category=assignment.category,
        questions=questions,
    )
