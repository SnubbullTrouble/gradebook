import os
import pytest

# Force tests to use in-memory SQLite database
os.environ.setdefault("DB_PATH", ":memory:")

from gradebook.database import models

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

# Initialize proxy to an in-memory DB; do not auto-create tables here — tests will manage schema
models.init_db(db_path=":memory:")


@pytest.fixture(autouse=True)
def reset_db():
    # Drop in an order that respects foreign keys, use safe=True to avoid errors
    real_db = db.obj if hasattr(db, "obj") else db

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
