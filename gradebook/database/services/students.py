from peewee import IntegrityError
from gradebook.database.models import Student
from gradebook.database.repositories import (
    get_all_students_dto as repo_get_all_students_dto,
    get_classes_for_student_dto as repo_get_classes_for_student_dto,
)
from gradebook.database.dtos import StudentDTO, ClassDTO


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


def create_student_dto(student_number: str, first_name: str, last_name: str):
    """Non-breaking helper that returns a StudentDTO from the repository."""
    from gradebook.database.repositories import create_student_dto as repo_create

    return repo_create(student_number, first_name, last_name)


def get_student_dto(student_number: str):
    """Non-breaking helper that returns a StudentDTO or None."""
    from gradebook.database.repositories import get_student_by_number_dto as repo_get

    return repo_get(student_number)


def get_all_students_dto() -> list[StudentDTO]:
    """Retrieve all students as DTOs."""
    return repo_get_all_students_dto()


def get_classes_for_student_dto(student_id: int) -> list[ClassDTO]:
    """Retrieve all classes a student is enrolled in as DTOs."""
    return repo_get_classes_for_student_dto(student_id)
