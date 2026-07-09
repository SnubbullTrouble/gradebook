import pytest
from peewee import IntegrityError
from gradebook.database.services.classes import create_class, enroll_student, get_number_of_students_in_class, get_all_classes, get_students_in_class, get_class_by_id
from gradebook.database.services.students import create_student
from gradebook.database.models import Class, Student


def test_create_and_get_class():
    c = create_class("Biology", None, None)
    assert c.name == "Biology"
    cls = get_class_by_id(c.id)
    assert cls.id == c.id


def test_enroll_and_count():
    c = create_class("History", None, None)
    s1 = create_student("S1", "A", "One")
    s2 = create_student("S2", "B", "Two")
    enroll_student(c, s1)
    enroll_student(c, s2)
    assert get_number_of_students_in_class(c) == 2


def test_get_students_in_class_returns_list():
    c = create_class("Chemistry", None, None)
    s = create_student("SX", "X", "Y")
    enroll_student(c, s)
    students = get_students_in_class(c.id)
    assert isinstance(students, list)
    assert students[0].student_number == "SX"
