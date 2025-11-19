"""
Class-related service functions.
"""

from __future__ import annotations
from typing import List
from models import Class, ClassRoster, Student


def create_class(name: str, term: str | None = None, teacher: str | None = None) -> Class:
    """Create a new class."""
    return Class.create(name=name, term=term, teacher=teacher)


def enroll_student(class_obj: Class, student_obj: Student) -> ClassRoster:
    """Enroll a student in a class (idempotent)."""
    roster_entry, _ = ClassRoster.get_or_create(class_ref=class_obj, student=student_obj)
    return roster_entry


def list_class_students(class_obj: Class) -> List[Student]:
    """Return a list of all students enrolled in a class."""
    return [cr.student for cr in class_obj.roster]
