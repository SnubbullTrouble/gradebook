from peewee import prefetch
from .models import (
    Assignment,
    AssignmentQuestion,
    Class,
    ClassAssignment,
    ClassRoster,
    Student,
    StudentQuestionScore,
    StudentAssignmentScore,
    AssignmentCategoryWeight,
)
from .dtos import (
    StudentDTO,
    AssignmentDTO,
    AssignmentQuestionDTO,
    ClassDTO,
    ClassAssignmentDTO,
    StudentAssignmentScoreDTO,
    StudentQuestionScoreDTO,
    AssignmentCategoryWeightDTO,
)


def create_student_dto(student_number: str, first_name: str, last_name: str) -> StudentDTO:
    s = Student.create(student_number=student_number, first_name=first_name, last_name=last_name)
    return StudentDTO(id=s.id, student_number=s.student_number, first_name=s.first_name, last_name=s.last_name)


def create_student(student_number: str, first_name: str, last_name: str) -> Student:
    return Student.create(student_number=student_number, first_name=first_name, last_name=last_name)


def get_student_by_number(student_number: str) -> Student | None:
    return Student.get_or_none(Student.student_number == student_number)


def get_student_by_number_dto(student_number: str) -> StudentDTO | None:
    s = get_student_by_number(student_number)
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


def get_all_classes_dto() -> list[ClassDTO]:
    return [
        ClassDTO(
            id=cls.id,
            name=cls.name,
            start_date=cls.start_date,
            end_date=cls.end_date,
        )
        for cls in Class.select()
    ]


def get_all_students_dto() -> list[StudentDTO]:
    return [
        StudentDTO(
            id=s.id,
            student_number=s.student_number,
            first_name=s.first_name,
            last_name=s.last_name,
        )
        for s in Student.select()
    ]


def get_students_for_class_dto(class_id: int) -> list[StudentDTO]:
    students = (
        Student.select()
        .join(ClassRoster)
        .join(Class)
        .where(Class.id == class_id)
    )
    return [
        StudentDTO(
            id=s.id,
            student_number=s.student_number,
            first_name=s.first_name,
            last_name=s.last_name,
        )
        for s in students
    ]


def get_classes_for_student_dto(student_id: int) -> list[ClassDTO]:
    classes = (
        Class.select()
        .join(ClassRoster)
        .where(ClassRoster.student == student_id)
    )
    return [
        ClassDTO(
            id=cls.id,
            name=cls.name,
            start_date=cls.start_date,
            end_date=cls.end_date,
        )
        for cls in classes
    ]


def get_class_assignment_dto(class_assignment_id: int) -> ClassAssignmentDTO | None:
    ca = ClassAssignment.get_or_none(ClassAssignment.id == class_assignment_id)
    if ca is None:
        return None
    return ClassAssignmentDTO(
        id=ca.id,
        class_id=ca.class_ref.id,
        assignment_id=ca.assignment.id,
        total_points=ca.total_points,
    )


def get_student_assignment_score_dto(score_id: int) -> StudentAssignmentScoreDTO | None:
    sas = StudentAssignmentScore.get_or_none(StudentAssignmentScore.id == score_id)
    if sas is None:
        return None
    return StudentAssignmentScoreDTO(
        id=sas.id,
        roster_entry_id=sas.roster_entry.id,
        class_assignment_id=sas.class_assignment.id,
        total_score=sas.total_score,
        total_time=sas.total_time,
    )


def get_student_question_score_dto(score_id: int) -> StudentQuestionScoreDTO | None:
    sqs = StudentQuestionScore.get_or_none(StudentQuestionScore.id == score_id)
    if sqs is None:
        return None
    return StudentQuestionScoreDTO(
        id=sqs.id,
        student_id=sqs.student.id,
        assignment_question_id=sqs.assignment_question.id,
        points_scored=sqs.points_scored,
    )


def get_student_question_scores_for_assignment_dto(
    assignment_id: int, student_id: int
) -> list[StudentQuestionScoreDTO]:
    scores = (
        StudentQuestionScore.select()
        .join(Student, on=(StudentQuestionScore.student == Student.id))
        .join(
            AssignmentQuestion,
            on=(StudentQuestionScore.assignment_question == AssignmentQuestion.id),
        )
        .join(Assignment, on=(AssignmentQuestion.assignment == Assignment.id))
        .where(Student.id == student_id, Assignment.id == assignment_id)
    )
    return [
        StudentQuestionScoreDTO(
            id=sqs.id,
            student_id=sqs.student.id,
            assignment_question_id=sqs.assignment_question.id,
            points_scored=sqs.points_scored,
        )
        for sqs in scores
    ]


def get_student_assignment_scores_for_student_dto(student_id: int) -> list[StudentAssignmentScoreDTO]:
    scores = (
        StudentAssignmentScore.select()
        .join(ClassRoster)
        .where(ClassRoster.student == student_id)
    )
    return [
        StudentAssignmentScoreDTO(
            id=sas.id,
            roster_entry_id=sas.roster_entry.id,
            class_assignment_id=sas.class_assignment.id,
            total_score=sas.total_score,
            total_time=sas.total_time,
        )
        for sas in scores
    ]


def get_class_by_id(class_id: int) -> Class | None:
    classes = (
        Class.select()
        .join(ClassRoster)
        .where(ClassRoster.student == student_id)
    )
    return [
        ClassDTO(
            id=cls.id,
            name=cls.name,
            start_date=cls.start_date,
            end_date=cls.end_date,
        )
        for cls in classes
    ]

def get_category_weight_dto(class_id: int, category: str) -> AssignmentCategoryWeightDTO | None:
    obj = AssignmentCategoryWeight.get_or_none(
        (AssignmentCategoryWeight.class_ref == class_id)
        & (AssignmentCategoryWeight.category == category)
    )
    if obj is None:
        return None
    return AssignmentCategoryWeightDTO(
        id=obj.id,
        class_id=obj.class_ref.id,
        category=obj.category,
        weight=obj.weight,
    )


def get_category_weights_for_class_dto(class_id: int) -> list[AssignmentCategoryWeightDTO]:
    weights = AssignmentCategoryWeight.select().where(
        AssignmentCategoryWeight.class_ref == class_id
    )
    return [
        AssignmentCategoryWeightDTO(
            id=w.id,
            class_id=w.class_ref.id,
            category=w.category,
            weight=w.weight,
        )
        for w in weights
    ]

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


def get_assignments_for_class_dto(class_id: int, category: str | None = None) -> list[AssignmentDTO]:
    assignments = fetch_assignments_for_class(class_id, category)
    return [
        AssignmentDTO(
            id=assignment.id,
            title=assignment.title,
            category=assignment.category,
            questions=get_questions_for_assignment_dto(assignment.id),
        )
        for assignment in assignments
    ]
