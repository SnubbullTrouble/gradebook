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


def get_student_by_number(student_number: str) -> Student:
    """
    Get a student by their student number within a specific class.

    Args:
        student_number: The student number to look up.

    Returns:
        Student: The matching Student object.

    Raises:
        Student.DoesNotExist: If no student with the given number exists in the class.
    """
    return Student.select().where((Student.student_number == student_number)).get()
