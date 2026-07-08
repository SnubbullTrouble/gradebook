from gradebook.database.services.assignments import get_assignment_dto, get_class_dto
from gradebook.database.services.assignments import create_assignment, assign_to_class
from gradebook.database.services.classes import create_class, enroll_student
from gradebook.database.services.students import create_student


def test_get_class_dto_returns_none_for_missing():
    assert get_class_dto(-1) is None


def test_get_assignment_dto_returns_none_for_missing():
    assert get_assignment_dto(-1) is None


def test_get_assignment_dto_after_creation():
    c = create_class("DTO Class")
    s = create_student("DTO5", "Data", "Tst")
    roster = enroll_student(c, s)
    a = create_assignment("DTO Assignment", "quiz", [5, 10])
    assign_to_class(c, a)
    dto = get_assignment_dto(a.id)
    assert dto is not None
    assert dto.id == a.id
    assert len(dto.questions) == 2
