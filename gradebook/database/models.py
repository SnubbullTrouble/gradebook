import os
from peewee import (
    Model,
    SqliteDatabase,
    AutoField,
    CharField,
    ForeignKeyField,
    FloatField,
    TextField,
    IntegerField,
    DateField,
)
from playhouse.db_url import connect
from playhouse.shortcuts import ReconnectMixin
from playhouse.pool import PooledDatabase
from peewee import DatabaseProxy

from enum import Enum

# Use a DatabaseProxy so tests and apps can initialize the real DB at runtime
db = DatabaseProxy()


def ensure_db_initialized(db_path: str | None = None, sqlite_uri: str | None = None, create_tables: bool = False):
    """Initialize the database proxy if needed and optionally create tables."""
    if getattr(db, "obj", None) is not None:
        return db.obj

    init_db(db_path=db_path, sqlite_uri=sqlite_uri, create_tables=create_tables)
    return db.obj


def init_db(db_path: str | None = None, sqlite_uri: str | None = None, create_tables: bool = False):
    """Initialize the database proxy.

    Provide either a file path (`db_path`) or a SQLite URI (`sqlite_uri`).
    If neither is provided, uses the `DB_PATH` env var or `gradebook.db`.

    If `create_tables` is True, creates all tables after initializing.
    """
    DB_PATH = db_path or os.getenv("DB_PATH", "gradebook.db")
    if sqlite_uri:
        real_db = SqliteDatabase(sqlite_uri)
    else:
        real_db = SqliteDatabase(DB_PATH)

    db.initialize(real_db)
    if create_tables:
        real_db.connect()
        real_db.create_tables(
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


class BaseModel(Model):
    """Base model class for Peewee."""

    class Meta:
        database = db


class Class(BaseModel):
    """Represents a class/course."""

    id = AutoField()
    name = CharField(unique=True)
    start_date = DateField(null=True)
    end_date = DateField(null=True)


class Student(BaseModel):
    """Represents a student."""

    id = AutoField()
    student_number = CharField(unique=True)
    first_name = CharField()
    last_name = CharField()


class ClassRoster(BaseModel):
    """Link between a Class and a Student."""

    id = AutoField()
    class_ref = ForeignKeyField(Class, backref="roster", on_delete="CASCADE")
    student = ForeignKeyField(Student, backref="classes", on_delete="CASCADE")

    class Meta:
        indexes = ((("class_ref", "student"), True),)  # unique constraint


class Assignment(BaseModel):
    """Represents an assignment."""

    id = AutoField()
    title = CharField()
    # centralize allowed categories
    ASSIGNMENT_CATEGORIES = [
        "quiz",
        "test",
        "homework",
        "final",
        "project",
        "attendance",
    ]

    category = CharField(choices=[(c, c) for c in ASSIGNMENT_CATEGORIES])


class Category(Enum):
    QUIZ = "quiz"
    TEST = "test"
    HOMEWORK = "homework"
    FINAL = "final"
    PROJECT = "project"
    ATTENDANCE = "attendance"
    # total_points = FloatField()


class AssignmentQuestion(BaseModel):
    """Represents a question for an assignment."""

    id = AutoField()
    assignment = ForeignKeyField(Assignment, backref="questions", on_delete="CASCADE")
    text = TextField()
    point_value = IntegerField()


class ClassAssignment(BaseModel):
    """Assignment assigned to a specific class."""

    id = AutoField()
    class_ref = ForeignKeyField(Class, backref="assignments", on_delete="CASCADE")
    assignment = ForeignKeyField(
        Assignment, backref="assigned_classes", on_delete="CASCADE"
    )
    total_points = FloatField(default=0.0)

    class Meta:
        indexes = ((("class_ref", "assignment"), True),)


class StudentAssignmentScore(BaseModel):
    """Tracks a student's score on a class assignment."""

    id = AutoField()
    roster_entry = ForeignKeyField(ClassRoster, backref="scores", on_delete="CASCADE")
    class_assignment = ForeignKeyField(
        ClassAssignment, backref="scores", on_delete="CASCADE"
    )
    total_score = FloatField()
    total_time = IntegerField(null=True)  # in seconds, optional


class StudentQuestionScore(BaseModel):
    """Stores a student's score for each question."""

    id = AutoField()
    student = ForeignKeyField(Student, backref="question_scores", on_delete="CASCADE")
    assignment_question = ForeignKeyField(
        AssignmentQuestion, backref="student_scores", on_delete="CASCADE"
    )
    points_scored = FloatField()

    class Meta:
        indexes = ((("student", "assignment_question"), True),)


class AssignmentCategoryWeight(BaseModel):
    """Stores weights for assignment categories for a class."""

    id = AutoField()
    class_ref = ForeignKeyField(Class, backref="category_weights", on_delete="CASCADE")
    category = CharField()  # quiz, test, homework
    weight = FloatField()

    class Meta:
        indexes = ((("class_ref", "category"), True),)


# NOTE: table creation is deliberatey not executed at import time.
# Call `init_db(create_tables=True)` from application/test setup to create tables.
