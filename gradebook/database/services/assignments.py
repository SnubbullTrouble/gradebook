from typing import List
from peewee import IntegrityError
from gradebook.database.models import Assignment, AssignmentQuestion, ClassAssignment, Class


def create_assignment(title: str, category: str, question_points: List[float]) -> Assignment:
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
    for idx, points in enumerate(question_points, start=1):
        AssignmentQuestion.create(
            assignment=assignment,
            text=f"Question {idx}",
            point_value=points
        )
    return assignment

def assign_to_class(cls: Class, assignment: Assignment) -> ClassAssignment:
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
        class_ref=cls,
        assignment=assignment,
        total_points=total_points
    )

