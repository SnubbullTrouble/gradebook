from gradebook.database.services.students import get_all_students_dto, get_classes_for_student_dto
from gradebook.database.services.classes import get_students_in_class_dto, get_all_classes_dto
from gradebook.database.services.students import create_student
from gradebook.database.services.classes import create_class, enroll_student
from gradebook.database.services.assignments import create_assignment, assign_to_class


def test_get_all_students_dto_returns_empty_list():
    assert get_all_students_dto() == []


def test_get_all_students_dto_returns_student_dtos():
    create_student("DTO2", "DT", "O")
    dtos = get_all_students_dto()
    assert len(dtos) == 1
    assert dtos[0].student_number == "DTO2"


def test_get_students_in_class_dto_returns_dtos():
    c = create_class("Roster DTO")
    s = create_student("DTO3", "DT", "O")
    enroll_student(c, s)
    student_dtos = get_students_in_class_dto(c.id)
    assert len(student_dtos) == 1
    assert student_dtos[0].student_number == "DTO3"


def test_get_classes_for_student_dto_returns_dtos():
    c = create_class("Class DTO")
    s = create_student("DTO4", "DT", "O")
    enroll_student(c, s)
    class_dtos = get_classes_for_student_dto(s.id)
    assert len(class_dtos) == 1
    assert class_dtos[0].name == "Class DTO"
