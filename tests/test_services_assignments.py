import pytest
from peewee import IntegrityError
from gradebook.database.services.assignments import create_assignment, assign_to_class, get_assignments_for_class, get_assignment_questions, get_assignment_questions_total_possible_points, get_assignment_weight
from gradebook.database.services.classes import create_class
from gradebook.database.services.students import create_student
from gradebook.database.services.classes import enroll_student


def test_create_assignment_with_int_list():
    a = create_assignment("Quiz", "quiz", [5, 10, 15])
    qs = list(get_assignment_questions(a.id))
    assert len(qs) == 3
    assert get_assignment_questions_total_possible_points(a.id) == 30


def test_assign_to_class_and_duplicate():
    c = create_class("Eng", None, None)
    a = create_assignment("Hw", "homework", [5])
    ca = assign_to_class(c, a)
    assert ca.class_ref.id == c.id
    with pytest.raises(IntegrityError):
        assign_to_class(c, a)


def test_get_assignments_for_class_filters_by_category():
    c = create_class("Comp", None, None)
    a1 = create_assignment("Q1", "quiz", [5])
    a2 = create_assignment("H1", "homework", [10])
    assign_to_class(c, a1)
    assign_to_class(c, a2)
    quizzes = get_assignments_for_class(c.id, category="quiz")
    assert any(a.title == "Q1" for a in quizzes)


def test_get_assignment_weight_default_zero():
    c = create_class("Stat", None, None)
    assert get_assignment_weight(c.id, "quiz") == 0.0
