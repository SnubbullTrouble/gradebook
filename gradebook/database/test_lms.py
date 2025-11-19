"""
Pytest module for testing the SQLite/Peewee LMS.
Covers:
- Class creation
- Student creation & enrollment
- Assignment templates & class assignment
- Question scoring
- Category weights and final grade
"""

from typing import Generator, Dict
import pytest
from peewee import SqliteDatabase

from models import (
    BaseModel,
    Class,
    Student,
    ClassRoster,
    Assignment,
    AssignmentQuestion,
    ClassAssignment,
    StudentAssignment,
    StudentAssignmentQuestion,
    AssignmentCategoryWeight,
    StudentCategoryScore,
)
from services.classes import create_class, enroll_student
from services.students import create_student
from services.assignments import create_assignment, assign_to_class
from services.scoring import record_full_assignment
from services.grades import set_category_weight, compute_weighted_grade


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")
def test_db() -> Generator[SqliteDatabase, None, None]:
    """
    Sets up a temporary in-memory database for testing.
    Tears down after each test function.
    """
    test_database = SqliteDatabase(":memory:")

    # Override the database in all models
    BaseModel._meta.database = test_database
    test_database.bind([
        Class,
        Student,
        ClassRoster,
        Assignment,
        AssignmentQuestion,
        ClassAssignment,
        StudentAssignment,
        StudentAssignmentQuestion,
        AssignmentCategoryWeight,
        StudentCategoryScore,
    ])
    test_database.connect()
    test_database.create_tables([
        Class,
        Student,
        ClassRoster,
        Assignment,
        AssignmentQuestion,
        ClassAssignment,
        StudentAssignment,
        StudentAssignmentQuestion,
        AssignmentCategoryWeight,
        StudentCategoryScore,
    ])
    yield test_database
    test_database.drop_tables([
        Class,
        Student,
        ClassRoster,
        Assignment,
        AssignmentQuestion,
        ClassAssignment,
        StudentAssignment,
        StudentAssignmentQuestion,
        AssignmentCategoryWeight,
        StudentCategoryScore,
    ])
    test_database.close()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_create_class_and_student(test_db: SqliteDatabase) -> None:
    """Test creating a class and enrolling a student."""
    c = create_class("Math 101", "Fall 2025")
    s = create_student("S1234", "John", "Doe")
    roster_entry = enroll_student(c, s)

    assert c.id is not None
    assert s.id is not None
    assert roster_entry.student.id == s.id
    assert roster_entry.class_ref.id == c.id
    assert len(list(c.roster)) == 1  # c.roster is a Peewee backref


def test_assignment_creation_and_class_assignment(test_db: SqliteDatabase) -> None:
    """Test creating an assignment template and assigning to a class."""
    c = create_class("Math 101")
    s = create_student("S1234", "John", "Doe")
    enroll_student(c, s)

    # Create assignment with 3 questions
    a = create_assignment("Quiz 1", "quiz", [5, 5, 10])
    ca = assign_to_class(c, a)

    assert a.id is not None
    assert len(list(a.questions)) == 3
    assert ca.total_points == sum(q.point_value for q in a.questions)


def test_record_scores_and_total(test_db: SqliteDatabase) -> None:
    """Test recording scores and computing total assignment score."""
    c = create_class("Math 101")
    s = create_student("S1234", "John", "Doe")
    roster_entry = enroll_student(c, s)

    a = create_assignment("Quiz 1", "quiz", [5, 5, 10])
    ca = assign_to_class(c, a)

    # Record full assignment scores
    q_scores: Dict[int, int] = {q.id: q.point_value for q in a.questions}
    sa, total = record_full_assignment(roster_entry, ca, q_scores)

    assert total == ca.total_points
    for saq in sa.question_scores:
        assert saq.score == saq.question.point_value


def test_category_weights_and_final_grade(test_db: SqliteDatabase) -> None:
    """Test setting category weights and computing final weighted grade."""
    c = create_class("Math 101")
    s = create_student("S1234", "John", "Doe")
    roster_entry = enroll_student(c, s)

    a = create_assignment("Quiz 1", "quiz", [5, 5, 10])
    ca = assign_to_class(c, a)  # assign only once

    q_scores: Dict[int, int] = {q.id: q.point_value for q in a.questions}
    record_full_assignment(roster_entry, ca, q_scores)  # reuse ca

    # Set weights
    set_category_weight(c, "quiz", 0.2)
    set_category_weight(c, "homework", 0.3)
    set_category_weight(c, "test", 0.5)

    grade = compute_weighted_grade(roster_entry)

    expected_points = sum(q.point_value for q in a.questions) * 0.2
    assert grade == expected_points

