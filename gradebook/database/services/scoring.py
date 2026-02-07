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
    Assignment,
)
from peewee import prefetch


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
        total_time=total_time,
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
    weights = {
        w.category: w.weight
        for w in AssignmentCategoryWeight.select().where(
            AssignmentCategoryWeight.class_ref == cls
        )
    }
    total_weight = sum(weights.values())
    if total_weight == 0:
        return 0.0

    # Gather all assignments for this student
    student_scores = (
        StudentAssignmentScore.select()
        .join(ClassRoster)
        .where(ClassRoster.id == cls_roster_entry.id)
    )
    category_totals: Dict[str, float] = {}
    category_max: Dict[str, float] = {}

    for score in student_scores:
        cat = score.class_assignment.assignment.category
        category_totals[cat] = category_totals.get(cat, 0.0) + score.total_score
        category_max[cat] = (
            category_max.get(cat, 0.0) + score.class_assignment.total_points
        )

    # Weighted average
    final_grade = 0.0
    for cat, weight in weights.items():
        cat_total = category_totals.get(cat, 0.0)
        cat_max = category_max.get(cat, 0.0)
        if cat_max > 0:
            final_grade += (cat_total / cat_max) * weight

    return final_grade / total_weight * 100


def get_student_scores_for_assignment(
    assignment_id: int, student_id: int
) -> list[StudentQuestionScore]:
    """
    Gets the question scores for an assignment for a student.

    Args:
        assignment_id (int): the assignment to grab
        student_id (int): the student to get questions for
    """
    # Get SQS for the student & assignment
    sqs_list = (
        StudentQuestionScore.select(StudentQuestionScore)
        .join(Student, on=(StudentQuestionScore.student == Student.id))
        .join(
            AssignmentQuestion,
            on=(StudentQuestionScore.assignment_question == AssignmentQuestion.id),
        )
        .join(Assignment, on=(AssignmentQuestion.assignment == Assignment.id))
        .where(Student.id == student_id, Assignment.id == assignment_id)
    )

    # Get all SAS rows for this assignment
    sas_list = (
        StudentAssignmentScore.select()
        .join(
            ClassAssignment,
            on=(StudentAssignmentScore.class_assignment == ClassAssignment.id),
        )
        .where(ClassAssignment.assignment == assignment_id)
    )

    # Attach SAS rows to SQS manually
    # We'll just attach all SAS rows to each SQS (since they all belong to the same assignment)
    for sqs in sqs_list:
        sqs.student_assignment_scores = sas_list

    return list(sqs_list)


def update_student_question_score(
    student_id: int, question_id: int, points_scored: float
) -> StudentQuestionScore:
    """
    Update a student's score for a particular question in an assignment.

    Args:
        student_id (int): ID of the student.
        question_id (int): ID of the question.
        points_scored (float): Points scored on this question.

    Returns:
        StudentQuestionScore: The updated or created score record.
    """
    sqs, created = StudentQuestionScore.get_or_create(
        student_id=student_id,
        assignment_question_id=question_id,
        defaults={"points_scored": points_scored},
    )
    if not created:
        sqs.points_scored = points_scored
        sqs.save()

    return sqs


def update_student_assignment_time(
    student_id: int, assignment_id: int, total_time: int
) -> StudentAssignmentScore:
    """
    Update a student's total time for an assignment.

    Args:
        student_id (int): ID of the student.
        assignment_id (int): ID of the assignment.
        total_time (int): Total time in seconds.

    Returns:
        StudentAssignmentScore: The updated score record with new total time.
    """
    sas = (
        StudentAssignmentScore.select()
        .join(
            ClassAssignment,
            on=(StudentAssignmentScore.class_assignment == ClassAssignment.id),
        )
        .join(ClassRoster, on=(StudentAssignmentScore.roster_entry == ClassRoster.id))
        .where(
            ClassRoster.student_id == student_id,
            ClassAssignment.assignment_id == assignment_id,
        )
        .first()
    )

    if sas:
        sas.total_time = total_time
        sas.save()
    return sas


def get_student_assignment_time(student_id: int, assignment_id: int) -> int:
    """
    Gets the total time a student took on an assignment.

    Args:
        student_id (int): ID of the student
        assignment_id (int): ID of the assignment

    Returns:
        int: Total time in seconds, or 0 if no record found
    """
    sas = (
        StudentAssignmentScore.select()
        .join(
            ClassAssignment,
            on=(StudentAssignmentScore.class_assignment == ClassAssignment.id),
        )
        .join(ClassRoster, on=(StudentAssignmentScore.roster_entry == ClassRoster.id))
        .where(
            ClassRoster.student_id == student_id,
            ClassAssignment.assignment_id == assignment_id,
        )
        .first()
    )

    if sas:
        return sas.total_time
    return 0
