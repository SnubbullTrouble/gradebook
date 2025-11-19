from typing import TYPE_CHECKING
from peewee import IntegrityError
from gradebook.database.models import Class, ClassRoster

if TYPE_CHECKING:
    from models import Student, ClassRoster


def create_class(name: str) -> Class:
    """
    Create a new class.

    Args:
        name: Name of the class.

    Returns:
        Class: The newly created Class object.

    Raises:
        IntegrityError: If a class with the same name already exists.
    """
    return Class.create(name=name)


def enroll_student(cls: Class, student: "Student") -> ClassRoster:
    """
    Enroll a student in a class.

    Args:
        cls: Class to enroll the student in.
        student: Student to enroll.

    Returns:
        ClassRoster: The enrollment record.

    Raises:
        IntegrityError: If the student is already enrolled in the class.
    """
    return ClassRoster.get_or_create(class_ref=cls, student=student)[0]
