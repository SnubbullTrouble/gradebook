"""
Student-related service functions.
"""

from models import Student


def create_student(student_number: str, first_name: str, last_name: str) -> Student:
    """Create a new student."""
    return Student.create(
        student_number=student_number,
        first_name=first_name,
        last_name=last_name
    )


def get_student_by_number(student_number: str) -> Student:
    """Look up a student by their student number."""
    return Student.get(Student.student_number == student_number)
