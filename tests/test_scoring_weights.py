from gradebook.database.services.assignments import create_assignment, assign_to_class
from gradebook.database.services.classes import create_class, enroll_student
from gradebook.database.services.students import create_student
from gradebook.database.services.scoring import (
    record_full_assignment,
    set_category_weight,
    compute_final_grade,
)


def test_weight_sum_not_one_still_computes():
    c = create_class("Weights 101")
    s = create_student("SW1", "W", "One")
    roster = enroll_student(c, s)
    a1 = create_assignment("Q", "quiz", [10])
    a2 = create_assignment("H", "homework", [20])
    ca1 = assign_to_class(c, a1)
    ca2 = assign_to_class(c, a2)
    record_full_assignment(roster, ca1, {q.id: q.point_value for q in a1.questions})
    record_full_assignment(roster, ca2, {q.id: q.point_value for q in a2.questions})
    set_category_weight(c, "quiz", 0.7)
    set_category_weight(c, "homework", 1.3)
    final = compute_final_grade(roster)
    assert 0 <= final <= 100
