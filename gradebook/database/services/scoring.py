from typing import Dict
from gradebook.database.models import (
    ClassRoster,
    ClassAssignment,
    StudentAssignmentScore,
    AssignmentCategoryWeight,
    Class,
    StudentQuestionScore,
    Student,
    AssignmentQuestion,
    Assignment
)


def record_full_assignment(
    roster_entry: ClassRoster,
    class_assignment: ClassAssignment,
    question_scores: Dict[int, float],
    total_time: int = None,
) -> StudentAssignmentScore:
    """
    Record a student's score for a full assignment.

    Args:
        roster_entry: ClassRoster entry for the student.
        class_assignment: ClassAssignment being scored.
        question_scores: Dict mapping AssignmentQuestion.id -> score

    Returns:
        StudentAssignmentScore: The total score recorded.
    """
    total_score = sum(question_scores.values())
    return StudentAssignmentScore.create(
        roster_entry=roster_entry,
        class_assignment=class_assignment,
        total_score=total_score,
        total_time=total_time
    )


def set_category_weight(
    cls: Class, category: str, weight: float
) -> AssignmentCategoryWeight:
    """
    Set the weight for a category in a class.

    Args:
        cls: Class for which the weight applies.
        category: "quiz", "test", or "homework".
        weight: Weight of this category.

    Returns:
        AssignmentCategoryWeight: The record created.
    """
    obj, _ = AssignmentCategoryWeight.get_or_create(
        class_ref=cls, category=category, defaults={"weight": weight}
    )
    obj.weight = weight
    obj.save()
    return obj


def compute_final_grade(cls_roster_entry: ClassRoster) -> float:
    """
    Compute the final weighted grade for a student in a class.

    Args:
        cls_roster_entry: ClassRoster entry for the student.

    Returns:
        float: Weighted final grade (0-100)
    """
    cls = cls_roster_entry.class_ref
    weights = {w.category: w.weight for w in AssignmentCategoryWeight.select().where(AssignmentCategoryWeight.class_ref == cls)}
    total_weight = sum(weights.values())
    if total_weight == 0:
        return 0.0

    # Gather all assignments for this student
    student_scores = StudentAssignmentScore.select().join(ClassRoster).where(ClassRoster.id == cls_roster_entry.id)
    category_totals: Dict[str, float] = {}
    category_max: Dict[str, float] = {}

    for score in student_scores:
        cat = score.class_assignment.assignment.category
        category_totals[cat] = category_totals.get(cat, 0.0) + score.total_score
        category_max[cat] = category_max.get(cat, 0.0) + score.class_assignment.total_points

    # Weighted average
    final_grade = 0.0
    for cat, weight in weights.items():
        cat_total = category_totals.get(cat, 0.0)
        cat_max = category_max.get(cat, 0.0)
        if cat_max > 0:
            final_grade += (cat_total / cat_max) * weight

    return final_grade / total_weight * 100

def get_student_scores_for_assignment(assignment_id: int, student_id: int) -> list[StudentQuestionScore]:
    '''
    Gets the question scores for an assignment for a student.

    Args:
        assignment_id (int): the assignment to grab
        student_id (int): the student to get questions for
    '''
    return list((
    StudentQuestionScore
    .select(StudentQuestionScore, StudentAssignmentScore)
    .join(Student)  # via StudentQuestionScore.student
    .switch(StudentQuestionScore)
    .join(AssignmentQuestion)  # via StudentQuestionScore.assignment_question
    .join(Assignment)  # via AssignmentQuestion.assignment
    .join(ClassAssignment)
    .join(StudentAssignmentScore)
    .where(
        Student.id == student_id,
        Assignment.id == assignment_id
    )
))

def get_student_assignment_score(student_id: int, assignment_id: int) -> StudentAssignmentScore:
    return list()[0]