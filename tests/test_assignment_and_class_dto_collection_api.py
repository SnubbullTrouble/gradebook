from gradebook.database.services.assignments import get_assignments_for_class_dto, get_assignment_question_dto
from gradebook.database.services.classes import get_all_classes_dto
from gradebook.database.services.assignments import create_assignment, assign_to_class
from gradebook.database.services.classes import create_class, enroll_student
from gradebook.database.services.students import create_student


def test_get_all_classes_dto_returns_empty_list_when_no_classes():
    assert get_all_classes_dto() == []


def test_get_all_classes_dto_returns_class_dtos():
    create_class("DTO Classes")
    dtos = get_all_classes_dto()
    assert len(dtos) == 1
    assert dtos[0].name == "DTO Classes"


def test_get_assignments_for_class_dto_returns_dtos():
    c = create_class("DTO Class List")
    create_student("DTO6", "Data", "Tst")
    a1 = create_assignment("DTO A1", "quiz", [5])
    a2 = create_assignment("DTO A2", "homework", [10])
    assign_to_class(c, a1)
    assign_to_class(c, a2)
    dtos = get_assignments_for_class_dto(c.id)
    assert len(dtos) == 2
    assert all(hasattr(dto, "questions") for dto in dtos)


def test_get_assignment_question_dto_returns_none_for_missing():
    assert get_assignment_question_dto(-1) is None
