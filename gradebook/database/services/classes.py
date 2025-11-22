from typing import TYPE_CHECKING
from peewee import IntegrityError
from gradebook.database.models import Class, ClassRoster
from datetime import datetime

if TYPE_CHECKING:
    from models import Student, ClassRoster

def create_class(name: str, start_date: datetime, end_date: datetime) -> Class:
    """
    Create a new class.

    Args:
        name: Name of the class.

    Returns:
        Class: The newly created Class object.

    Raises:
        IntegrityError: If a class with the same name already exists.
    """
    return Class.create(name=name, start_date=start_date, end_date=end_date)


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

def get_all_classes() -> list[Class]:
    """
    Retrieve all classes.

    Returns:
        list[Class]: List of all Class objects.
    """
    return list(Class.select())

def get_number_of_students_in_class(cls: Class) -> int:
    """
    Get the number of students enrolled in a class.

    Args:
        cls (models.Class): Class to count students in.

    Returns:
        int: Number of students enrolled in the class.
    """
    return ClassRoster.select().where(ClassRoster.class_ref == cls).count()