import pytest
from peewee import IntegrityError
from gradebook.database.models import (
    db,
    Class,
    Student,
    ClassRoster,
    Assignment,
    AssignmentQuestion,
    ClassAssignment,
    StudentAssignmentScore,
    AssignmentCategoryWeight
)
from gradebook.database.services.classes import create_class, enroll_student
from gradebook.database.services.students import create_student
from gradebook.database.services.assignments import create_assignment, assign_to_class
from gradebook.database.services.scoring import record_full_assignment, set_category_weight, compute_final_grade


@pytest.fixture(autouse=True)
def reset_db():
    """Reset the database before each test."""
    db.drop_tables([
        ClassRoster, ClassAssignment, StudentAssignmentScore, AssignmentCategoryWeight,
        AssignmentQuestion, Assignment, Student, Class
    ])
    db.create_tables([
        Class, Student, ClassRoster, Assignment, AssignmentQuestion, ClassAssignment,
        StudentAssignmentScore, AssignmentCategoryWeight
    ])
    yield


def test_create_class_and_student():
    c = create_class("Math 101")
    s = create_student("S123", "Alice", "Smith")
    assert c.name == "Math 101"
    assert s.student_number == "S123"


def test_enroll_student_success():
    c = create_class("Physics")
    s = create_student("S456", "Bob", "Jones")
    roster_entry = enroll_student(c, s)
    assert roster_entry.class_ref == c
    assert roster_entry.student == s


def test_duplicate_enrollment_returns_existing():
    c = create_class("History")
    s = create_student("S789", "Charlie", "Brown")
    entry1 = enroll_student(c, s)
    entry2 = enroll_student(c, s)
    assert entry1.id == entry2.id


def test_create_assignment():
    a = create_assignment("Quiz 1", "quiz", [5, 5, 10])
    assert a.title == "Quiz 1"
    assert len(a.questions) == 3


def test_assign_to_class_success():
    c = create_class("Chemistry")
    a = create_assignment("Test 1", "test", [10, 15])
    class_assignment = assign_to_class(c, a)
    assert class_assignment.class_ref == c
    assert class_assignment.assignment == a


def test_duplicate_class_assignment_raises():
    c = create_class("Biology")
    a = create_assignment("Homework 1", "homework", [5, 5])
    assign_to_class(c, a)
    with pytest.raises(IntegrityError):
        assign_to_class(c, a)


def test_record_full_assignment_success():
    c = create_class("English")
    s = create_student("S111", "Daisy", "Miller")
    roster = enroll_student(c, s)
    a = create_assignment("Essay 1", "homework", [20])
    class_assignment = assign_to_class(c, a)
    scores = {q.id: q.point_value for q in a.questions}
    record = record_full_assignment(roster, class_assignment, scores, total_time=3600)
    assert record.total_score == sum(scores.values())


def test_record_assignment_for_non_enrolled_student_raises():
    c = create_class("Geography")
    s = create_student("S222", "Evan", "Peters")
    a = create_assignment("Quiz 2", "quiz", [5])
    class_assignment = assign_to_class(c, a)
    with pytest.raises(IntegrityError):
        record_full_assignment(ClassRoster(class_ref=c, student=s), class_assignment, {1: 5}, total_time=600)


def test_set_category_weight_and_compute_grade():
    c = create_class("Math 201")
    s = create_student("S333", "Fiona", "Green")
    roster = enroll_student(c, s)
    a1 = create_assignment("Quiz 1", "quiz", [5, 5])
    a2 = create_assignment("Homework 1", "homework", [10])
    ca1 = assign_to_class(c, a1)
    ca2 = assign_to_class(c, a2)
    record_full_assignment(roster, ca1, {q.id: q.point_value for q in a1.questions}, total_time=1200)
    record_full_assignment(roster, ca2, {q.id: q.point_value for q in a2.questions}, total_time=1800)
    set_category_weight(c, "quiz", 0.7)
    set_category_weight(c, "homework", 0.3)
    final_grade = compute_final_grade(roster)
    assert 0 <= final_grade <= 100


def test_compute_grade_with_multiple_assignments_and_types():
    c = create_class("CS101")
    s = create_student("S444", "George", "Harrison")
    roster = enroll_student(c, s)
    a1 = create_assignment("Quiz 1", "quiz", [10, 10])
    a2 = create_assignment("Test 1", "test", [20])
    a3 = create_assignment("Homework 1", "homework", [5, 5, 5])
    assign_to_class(c, a1)
    assign_to_class(c, a2)
    assign_to_class(c, a3)
    for a in [a1, a2, a3]:
        ca = ClassAssignment.get(class_ref=c, assignment=a)
        record_full_assignment(roster, ca, {q.id: q.point_value for q in a.questions}, total_time=1500)
    set_category_weight(c, "quiz", 0.2)
    set_category_weight(c, "test", 0.5)
    set_category_weight(c, "homework", 0.3)
    final_grade = compute_final_grade(roster)
    assert 0 <= final_grade <= 100


def test_assignment_with_zero_questions():
    c = create_class("Philosophy")
    s = create_student("S555", "Hannah", "Ivers")
    roster = enroll_student(c, s)
    a = create_assignment("Empty Assignment", "homework", [])
    ca = assign_to_class(c, a)
    record = record_full_assignment(roster, ca, {}, total_time=0)
    assert record.total_score == 0


def test_student_with_no_assignments():
    c = create_class("Art")
    s = create_student("S666", "Ian", "Jackson")
    roster = enroll_student(c, s)
    final_grade = compute_final_grade(roster)
    assert final_grade == 0
