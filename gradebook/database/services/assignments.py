import dataclasses
from typing import List
from gradebook.database.models import (
    Assignment,
    AssignmentCategoryWeight,
    AssignmentQuestion,
    ClassAssignment,
    Class,
)
from gradebook.database.models import db
from peewee import IntegrityError
from peewee import prefetch
from gradebook.database.services import scoring
from gradebook.database.repositories import (
    fetch_assignments_for_class,
    get_assignment_dto as repo_get_assignment_dto,
    get_class_dto as repo_get_class_dto,
    get_assignment_question_dto as repo_get_assignment_question_dto,
    get_questions_for_assignment_dto as repo_get_questions_for_assignment_dto,
    get_assignments_for_class_dto as repo_get_assignments_for_class_dto,
    get_category_weight_dto as repo_get_category_weight_dto,
    get_category_weights_for_class_dto as repo_get_category_weights_for_class_dto,
)


@dataclasses.dataclass
class Question:
    question: str
    points: int


def create_assignment(
    title: str, category: str, questions: List[Question] | List[int] | None
) -> Assignment:
    """
    Create an assignment with multiple questions.

    Args:
        title: Assignment title.
        category: "quiz", "test", or "homework".
        question_points: List of point values for each question.

    Returns:
        Assignment: The created Assignment object.
    """
    if category not in Assignment.ASSIGNMENT_CATEGORIES:
        raise ValueError(
            f"Invalid category '{category}'. Allowed: {Assignment.ASSIGNMENT_CATEGORIES}"
        )

    # create within a transaction to ensure questions and assignment persist together
    with db.atomic():
        assignment = Assignment.create(title=title, category=category)
        if not questions:
            return assignment

        for idx, q in enumerate(questions, start=1):
            if isinstance(q, Question):
                text = q.question
                points = q.points
            elif isinstance(q, int):
                text = f"Question {idx}"
                points = q
            elif isinstance(q, (tuple, list)) and len(q) >= 2:
                text = str(q[0])
                points = int(q[1])
            else:
                try:
                    points = int(q)
                except Exception:
                    points = 0
                text = f"Question {idx}"

            AssignmentQuestion.create(
                assignment=assignment, text=text, point_value=points
            )
    return assignment


def assign_to_class(cls: "Class", assignment: Assignment) -> ClassAssignment:
    """
    Assign an assignment template to a class.

    Duplicate assignments for the same class should raise IntegrityError.

    Args:
        cls (Class): The class to assign the assignment to.
        assignment (Assignment): The assignment template.

    Returns:
        ClassAssignment: The created class-assignment record.

    Raises:
        IntegrityError: If the assignment is already linked to the class.
    """
    total_points = sum(q.point_value for q in assignment.questions)

    # This will raise IntegrityError if the class_ref/assignment combination already exists.
    # Create inside a transaction to ensure consistency
    with db.atomic():
        return ClassAssignment.create(
            class_ref=cls, assignment=assignment, total_points=total_points
        )


def get_assignments_for_class(class_id: int, category: str = None) -> list[Assignment]:
    """
    Gets a list of assignments for the provided class id

    Args:
        class_id (int): id of the class to filter on
        category (str): category to filter on (optional)

    Returns:
        list(Assignment): the list of assignments for this class (and category, if provided)
    """
    return fetch_assignments_for_class(class_id, category)


def get_assignment_dto(assignment_id: int):
    """Retrieve an assignment DTO by its ID."""
    return repo_get_assignment_dto(assignment_id)


def get_assignments_for_class_dto(class_id: int, category: str = None):
    """Retrieve assignment DTOs for a class."""
    return repo_get_assignments_for_class_dto(class_id, category)


def get_assignment_question_dto(question_id: int):
    """Retrieve a question DTO by its ID."""
    return repo_get_assignment_question_dto(question_id)


def get_questions_for_assignment_dto(assignment_id: int):
    """Retrieve question DTOs for an assignment."""
    return repo_get_questions_for_assignment_dto(assignment_id)


def get_class_dto(class_id: int):
    """Retrieve a class DTO by its ID."""
    return repo_get_class_dto(class_id)


def get_category_weight_dto(class_id: int, category: str):
    """Retrieve category weight DTO for a class and category."""
    return repo_get_category_weight_dto(class_id, category)


def get_category_weights_for_class_dto(class_id: int):
    """Retrieve category weight DTOs for a class."""
    return repo_get_category_weights_for_class_dto(class_id)


def get_assignment_questions(assignment_id) -> list[AssignmentQuestion]:
    """
    Gets the assignment questions for a particular assignment

    Args:
        assignment_id (int): the assignment to grab

    Returns:
        list(AssignmentQuestion): the questions in the assignment
    """
    return list(
        AssignmentQuestion.select()
        .join(Assignment)
        .where(Assignment.id == assignment_id)
    )


def get_student_category_score(student_id: int, class_id: int, category: str) -> int:
    """
    Gets the total score for a student in a class for a particular category.

    Args:
        student_id (int): the student to get the score for
        class_id (int): the class to get the score for
        category (str): the category to get the score for

    Returns:
        int: the total score for the student in the given category for the given class
    """
    # Get all the assignments for the class and category
    assignments = get_assignments_for_class(class_id, category)

    # Get all the scores for the student for those assignments
    total_score = 0
    total_possible = 0
    for assignment in assignments:
        # Get the score for each question in the assignment or 0 if not scored
        points_scored = scoring.get_student_scores_for_assignment(
            assignment.id, student_id
        )
        total_score += (
            sum([_.points_scored for _ in points_scored]) if points_scored else 0
        )

        # Get the total possible points for the assignment
        total_possible += get_assignment_questions_total_possible_points(assignment.id)

    return total_score if total_possible == 0 else total_score / total_possible * 100


def get_assignment_questions_total_possible_points(assignment_id: int) -> int:
    """
    Gets the total possible points for an assignment by summing the point values of its questions.

    Args:
        assignment_id (int): the ID of the assignment to calculate total points for

    Returns:
        int: the total possible points for the assignment
    """
    return sum(
        q.point_value
        for q in AssignmentQuestion.select()
        .join(Assignment)
        .where(Assignment.id == assignment_id)
    )


def get_assignment_weight(class_id: int, category: str) -> float:
    """
    Gets the weight for a particular category in a class.

    Args:
        class_id (int): the class to get the weight for
        category (str): the category to get the weight for

    Returns:
        float: the weight for the category in the class
    """
    obj = (
        AssignmentCategoryWeight.select()
        .where(
            (AssignmentCategoryWeight.category == category)
            & (AssignmentCategoryWeight.class_ref == class_id)
        )
        .first()
    )

    return obj.weight if obj else 0.0
