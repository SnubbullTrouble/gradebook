from peewee import IntegrityError
from gradebook.database.models import Student


def create_student(student_number: str, first_name: str, last_name: str) -> Student:
    """
    Create a new student.

    Args:
        student_number: Unique identifier for the student.
        first_name: First name.
        last_name: Last name.

    Returns:
        Student: Newly created Student object.

    Raises:
        IntegrityError: If a student with the same student_number already exists.
    """
    return Student.create(
        student_number=student_number, first_name=first_name, last_name=last_name
    )
