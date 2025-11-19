"""
Scoring and grading for student assignments.
"""

from __future__ import annotations
from typing import Dict, Tuple
from models import (
    StudentAssignment, StudentAssignmentQuestion,
    ClassRoster, ClassAssignment, AssignmentQuestion
)


def create_student_assignment(
    roster_entry: ClassRoster,
    class_assignment: ClassAssignment
) -> StudentAssignment:
    """Create or retrieve a StudentAssignment record."""
    sa, _ = StudentAssignment.get_or_create(
        roster_entry=roster_entry,
        class_assignment=class_assignment,
    )
    return sa


def record_question_score(
    student_assignment: StudentAssignment,
    question: AssignmentQuestion,
    score: float
) -> StudentAssignmentQuestion:
    """Record or update a score for a specific question."""
    saq, _ = StudentAssignmentQuestion.get_or_create(
        student_assignment=student_assignment,
        question=question
    )
    saq.score = score
    saq.save()
    return saq


def recompute_total(student_assignment: StudentAssignment) -> float:
    """Recalculate and update a student's total assignment score."""
    total = sum((qs.score or 0) for qs in student_assignment.question_scores)
    student_assignment.total_score = total
    student_assignment.save()
    return total


def record_full_assignment(
    roster_entry: ClassRoster,
    class_assignment: ClassAssignment,
    scores_dict: Dict[int, float]
) -> Tuple[StudentAssignment, float]:
    """
    Record scores for all questions in an assignment.

    Args:
        roster_entry: The student's roster record.
        class_assignment: The class-assignment link.
        scores_dict: {question_id: score}

    Returns:
        (StudentAssignment, total_score)
    """
    sa = create_student_assignment(roster_entry, class_assignment)

    for qid, score in scores_dict.items():
        question = AssignmentQuestion.get_by_id(qid)
        record_question_score(sa, question, score)

    total = recompute_total(sa)
    return sa, total
