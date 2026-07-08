import pytest
from peewee import IntegrityError
from gradebook.database.services.students import create_student, get_student_by_number
from gradebook.database.models import Student


def test_create_student_and_lookup():
    s = create_student("ST100", "Test", "User")
    assert s.student_number == "ST100"


def test_duplicate_student_number_raises():
    create_student("ST200", "A", "B")
    with pytest.raises(IntegrityError):
        create_student("ST200", "C", "D")


def test_get_student_by_number_not_found_raises():
    with pytest.raises(Student.DoesNotExist):
        get_student_by_number("NO_SUCH")
