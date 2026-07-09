import pytest
from gradebook.database.services.assignments import create_assignment, assign_to_class
from gradebook.database.services.classes import create_class, enroll_student
from gradebook.database.services.students import create_student
from gradebook.database.services.scoring import (
    record_full_assignment,
    StudentAssignmentScore,
)
from gradebook.database.models import StudentQuestionScore


def test_record_full_assignment_creates_question_scores():
    c = create_class("Consistency")
    s = create_student("SC1", "Cons", "Tst")
    roster = enroll_student(c, s)
    a = create_assignment("ConsA", "quiz", [5, 5])
    ca = assign_to_class(c, a)
    qs = {q.id: q.point_value for q in a.questions}
    rec = record_full_assignment(roster, ca, qs, total_time=100)
    # aggregate exists
    assert isinstance(rec, StudentAssignmentScore.__class__) or rec is not None
    # per-question scores exist
    sqs = list(StudentQuestionScore.select().where(StudentQuestionScore.student == s))
    assert len(sqs) == 2
    assert sum(qs.values()) == rec.total_score


def test_transactional_rollback_on_failure(monkeypatch):
    c = create_class("Rollback")
    s = create_student("RB1", "Roll", "Back")
    roster = enroll_student(c, s)
    a = create_assignment("RB", "quiz", [2, 3])
    ca = assign_to_class(c, a)
    qs = {q.id: q.point_value for q in a.questions}

    # force StudentAssignmentScore.create to raise to simulate failure after per-question writes
    original_create = StudentAssignmentScore.create

    def raising_create(*args, **kwargs):
        raise RuntimeError("simulated failure")

    monkeypatch.setattr("gradebook.database.services.scoring.StudentAssignmentScore.create", raising_create)

    with pytest.raises(RuntimeError):
        record_full_assignment(roster, ca, qs)

    # ensure no StudentQuestionScore rows persisted due to rollback
    sqs_after = list(StudentQuestionScore.select().where(StudentQuestionScore.student == s))
    assert len(sqs_after) == 0

    # restore original create
    monkeypatch.setattr("gradebook.database.services.scoring.StudentAssignmentScore.create", original_create)
