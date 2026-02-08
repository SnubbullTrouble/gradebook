import dataclasses
from typing import List
from gradebook.database.models import (
    Assignment,
    AssignmentCategoryWeight,
    AssignmentQuestion,
    ClassAssignment,
    Class,
)
from gradebook.database.services import scoring


@dataclasses.dataclass
class Question:
    question: str
    points: int


def create_assignment(
    title: str, category: str, questions: List[Question]
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
    assignment = Assignment.create(title=title, category=category)
    for q in questions:
        AssignmentQuestion.create(
            assignment=assignment, text=q.question, point_value=q.points
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
    if category:
        return list(
            Assignment.select()
            .join(ClassAssignment)
            .join(Class)
            .where((Assignment.category == category) & (Class.id == class_id))
        )
    else:
        return list(
            Assignment.select()
            .join(ClassAssignment)
            .join(Class)
            .where(Class.id == class_id)
        )


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
