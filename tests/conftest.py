import os
import pytest

# Force tests to use in-memory SQLite database
os.environ.setdefault("DB_PATH", ":memory:")

from gradebook.database import models  # ensure models import happens after DB_PATH set

from gradebook.database.models import (
    db,
    Class,
    Student,
    ClassRoster,
    Assignment,
    AssignmentQuestion,
    ClassAssignment,
    StudentAssignmentScore,
    AssignmentCategoryWeight,
    StudentQuestionScore,
)


@pytest.fixture(autouse=True)
def reset_db():
    # Drop in an order that respects foreign keys, use safe=True to avoid errors
    db.drop_tables(
        [
            StudentQuestionScore,
            StudentAssignmentScore,
            ClassAssignment,
            AssignmentQuestion,
            AssignmentCategoryWeight,
            Assignment,
            ClassRoster,
            Student,
            Class,
        ],
        safe=True,
    )
    db.create_tables(
        [
            Class,
            Student,
            ClassRoster,
            Assignment,
            AssignmentQuestion,
            ClassAssignment,
            StudentAssignmentScore,
            AssignmentCategoryWeight,
            StudentQuestionScore,
        ]
    )
    yield
