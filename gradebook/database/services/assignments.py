"""
Assignment-related service functions.
"""

from __future__ import annotations
from typing import Dict, Iterable, List
from models import (
    Assignment, AssignmentQuestion,
    ClassAssignment, Class, AssignmentType
)


def create_assignment(title: str, type: str | AssignmentType, questions: Iterable[float] | Dict[int, float]) -> Assignment:
    """
    Create an assignment template with questions.

    Args:
        title: Assignment title.
        type: AssignmentType or string.
        questions: Either a dict {qnum: points} or a list of point values.

    Returns:
        Assignment
    """
    if not isinstance(type, str):
        type = type.value

    assignment = Assignment.create(title=title, type=type)

    # Create questions
    if isinstance(questions, dict):
        for qnum, pts in questions.items():
            AssignmentQuestion.create(
                assignment=assignment,
                question_number=qnum,
                point_value=pts,
            )
    else:
        for i, pts in enumerate(questions, start=1):
            AssignmentQuestion.create(
                assignment=assignment,
                question_number=i,
                point_value=pts,
            )

    return assignment


def assign_to_class(class_obj: Class, assignment_obj: Assignment, due_date: str | None = None) -> ClassAssignment:
    """
    Assign a reusable assignment to a class.
    Computes and stores total points automatically.
    """
    total = sum(q.point_value for q in assignment_obj.questions)

    return ClassAssignment.create(
        class_ref=class_obj,
        assignment=assignment_obj,
        due_date=due_date,
        total_points=total
    )


def list_class_assignments(class_obj: Class) -> List[Assignment]:
    """Return all assignments linked to a class."""
    return [ca.assignment for ca in class_obj.assignments]
