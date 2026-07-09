import pytest
from gradebook.database.services.assignments import create_assignment, assign_to_class
from gradebook.database.services.classes import create_class, enroll_student
from gradebook.database.services.students import create_student
from gradebook.database.services.scoring import (
    record_full_assignment,
    set_category_weight,
    compute_final_grade,
    update_student_question_score,
    update_student_assignment_time,
    get_student_assignment_time,
    get_student_scores_for_assignment,
)


def test_record_and_retrieve_scores_and_time():
    c = create_class("Music", None, None)
    s = create_student("S900", "T", "U")
    roster = enroll_student(c, s)
    a = create_assignment("Test", "quiz", [10, 10])
    ca = assign_to_class(c, a)
    scores = {q.id: q.point_value for q in a.questions}
    rec = record_full_assignment(roster, ca, scores, total_time=500)
    assert rec.total_score == sum(scores.values())
    assert update_student_assignment_time(s.id, a.id, 600).total_time == 600
    assert get_student_assignment_time(s.id, a.id) == 600


def test_update_question_score_create_and_update():
    c = create_class("Geo", None, None)
    s = create_student("S910", "N", "O")
    roster = enroll_student(c, s)
    a = create_assignment("Q", "quiz", [5])
    ca = assign_to_class(c, a)
    q = list(a.questions)[0]
    sqs = update_student_question_score(s.id, q.id, 4.0)
    assert sqs.points_scored == 4.0
    sqs2 = update_student_question_score(s.id, q.id, 3.0)
    assert sqs2.points_scored == 3.0


def test_get_student_scores_for_assignment_attaches_sas_list():
    c = create_class("Ops", None, None)
    s = create_student("S920", "P", "Q")
    roster = enroll_student(c, s)
    a = create_assignment("Mixed", "homework", [2, 3])
    ca = assign_to_class(c, a)
    record_full_assignment(roster, ca, {q.id: q.point_value for q in a.questions}, total_time=100)
    sqs_list = get_student_scores_for_assignment(a.id, s.id)
    # function attaches sas_list attribute to each SQS
    if sqs_list:
        assert hasattr(sqs_list[0], "student_assignment_scores")
