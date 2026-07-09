from gradebook.database.services.scoring import (
    get_class_assignment_dto,
    get_student_assignment_score_dto,
    get_student_question_score_dto,
    get_student_question_scores_for_assignment_dto,
    get_student_assignment_scores_for_student_dto,
    record_full_assignment,
)
from gradebook.database.services.assignments import create_assignment, assign_to_class
from gradebook.database.services.classes import create_class, enroll_student
from gradebook.database.services.students import create_student


def test_get_class_assignment_dto_returns_none_for_missing():
    assert get_class_assignment_dto(-1) is None


def test_get_student_question_score_dto_returns_none_for_missing():
    assert get_student_question_score_dto(-1) is None


def test_scoring_dto_paths_after_record():
    c = create_class("Scoring DTO")
    s = create_student("DTO7", "Data", "Tst")
    roster = enroll_student(c, s)
    a = create_assignment("DTO Score", "quiz", [5, 5])
    ca = assign_to_class(c, a)
    rec = record_full_assignment(roster, ca, {q.id: q.point_value for q in a.questions}, total_time=120)

    class_assignment_dto = get_class_assignment_dto(ca.id)
    assert class_assignment_dto is not None
    assert class_assignment_dto.id == ca.id

    sas_dto = get_student_assignment_score_dto(rec.id)
    assert sas_dto is not None
    assert sas_dto.total_score == rec.total_score

    question_dtos = get_student_question_scores_for_assignment_dto(a.id, s.id)
    assert isinstance(question_dtos, list)
    assert len(question_dtos) == 2

    student_assignment_scores = get_student_assignment_scores_for_student_dto(s.id)
    assert len(student_assignment_scores) == 1
