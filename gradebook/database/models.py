"""
Database models for a SQLite-based Learning Management System (LMS).
Implements:
- Students (+ student numbers)
- Classes and rosters
- Reusable assignments + questions
- Class-assignment linking
- Student submissions and per-question scores
- Category weights and student category totals

Uses Peewee ORM.
"""

from __future__ import annotations
from typing import Optional
from enum import Enum
from peewee import *


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

db = SqliteDatabase("school.db")


# ---------------------------------------------------------------------------
# ENUMS
# ---------------------------------------------------------------------------

class AssignmentType(str, Enum):
    """Enumeration of assignment types."""
    QUIZ = "quiz"
    TEST = "test"
    HOMEWORK = "homework"


# ---------------------------------------------------------------------------
# Base Model
# ---------------------------------------------------------------------------

class BaseModel(Model):
    """Base model for all Peewee models ensuring they use the shared database."""
    class Meta:
        database = db


# ---------------------------------------------------------------------------
# Core Models
# ---------------------------------------------------------------------------

class Class(BaseModel):
    """Represents a class (course)."""
    name: str = CharField()
    term: Optional[str] = CharField(null=True)
    teacher: Optional[str] = CharField(null=True)


class Student(BaseModel):
    """Represents a student with a unique student number."""
    student_number: str = CharField(unique=True)
    first_name: str = CharField()
    last_name: str = CharField()


class ClassRoster(BaseModel):
    """
    Links students to classes (many-to-many).
    Prevents duplicates with a unique index.
    """
    class_ref: Class = ForeignKeyField(Class, backref="roster", on_delete="CASCADE")
    student: Student = ForeignKeyField(Student, backref="classes", on_delete="CASCADE")

    class Meta:
        indexes = ((( "class_ref", "student" ), True),)


# ---------------------------------------------------------------------------
# Assignment Definitions (Reusable Templates)
# ---------------------------------------------------------------------------

class Assignment(BaseModel):
    """A reusable assignment definition (template)."""
    title: str = CharField()
    type: str = CharField(choices=[t.value for t in AssignmentType])


class AssignmentQuestion(BaseModel):
    """Represents a question belonging to an assignment."""
    assignment: Assignment = ForeignKeyField(Assignment, backref="questions", on_delete="CASCADE")
    question_number: int = IntegerField()
    point_value: float = FloatField()


# ---------------------------------------------------------------------------
# Class-Assignment Linking
# ---------------------------------------------------------------------------

class ClassAssignment(BaseModel):
    """
    Associates a reusable assignment with a specific class.
    Contains per-class metadata like due dates and total points.
    """
    class_ref: Class = ForeignKeyField(Class, backref="assignments", on_delete="CASCADE")
    assignment: Assignment = ForeignKeyField(Assignment, backref="class_links", on_delete="CASCADE")
    due_date: Optional[str] = DateField(null=True)
    total_points: Optional[float] = FloatField(null=True)

    class Meta:
        indexes = ((( "class_ref", "assignment" ), True),)


# ---------------------------------------------------------------------------
# Student Assignments + Score Records
# ---------------------------------------------------------------------------

class StudentAssignment(BaseModel):
    """Represents a student's submission for an assignment."""
    roster_entry: ClassRoster = ForeignKeyField(ClassRoster, backref="assignments", on_delete="CASCADE")
    class_assignment: ClassAssignment = ForeignKeyField(ClassAssignment, backref="student_assignments", on_delete="CASCADE")
    total_score: Optional[float] = FloatField(null=True)

    class Meta:
        indexes = ((( "roster_entry", "class_assignment" ), True),)


class StudentAssignmentQuestion(BaseModel):
    """Score for a student's response to a specific question."""
    student_assignment: StudentAssignment = ForeignKeyField(
        StudentAssignment, backref="question_scores", on_delete="CASCADE"
    )
    question: AssignmentQuestion = ForeignKeyField(
        AssignmentQuestion, backref="student_scores", on_delete="CASCADE"
    )
    score: Optional[float] = FloatField(null=True)

    class Meta:
        indexes = ((( "student_assignment", "question" ), True),)


# ---------------------------------------------------------------------------
# Category Weights + Student Totals
# ---------------------------------------------------------------------------

class AssignmentCategoryWeight(BaseModel):
    """Weight for each assignment type for a given class."""
    class_ref: Class = ForeignKeyField(Class, backref="category_weights", on_delete="CASCADE")
    type: str = CharField(choices=[t.value for t in AssignmentType])
    weight: float = FloatField()

    class Meta:
        indexes = ((( "class_ref", "type" ), True),)


class StudentCategoryScore(BaseModel):
    """Stores total points per assignment category for a student."""
    roster_entry: ClassRoster = ForeignKeyField(ClassRoster, backref="category_scores", on_delete="CASCADE")
    type: str = CharField(choices=[t.value for t in AssignmentType])
    total_score: float = FloatField(default=0.0)

    class Meta:
        indexes = ((( "roster_entry", "type" ), True),)


# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------

def initialize_db() -> None:
    """Create all database tables."""
    with db:
        db.create_tables([
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
