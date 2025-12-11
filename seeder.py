import os
from datetime import date, timedelta
from random import randint, uniform, choice
from faker import Faker

from gradebook.database.models import (
    db,
    Class,
    Student,
    ClassRoster,
    Assignment,
    AssignmentQuestion,
    ClassAssignment,
    StudentAssignmentScore,
    StudentQuestionScore,
    AssignmentCategoryWeight,
)

fake = Faker()


# -----------------------------------------------------
# Database reset
# -----------------------------------------------------
def reset_database():
    db_path = os.getenv("DB_PATH", "gradebook.db")  # or db.database for Peewee >=3.15

    # Close if already open
    if not db.is_closed():
        db.close()

    # Safety check
    if os.path.exists(db_path):
        print(f"Removing old database at {db_path} ...")
        os.remove(db_path)

    print(f"Connecting to database at {db_path} ...")
    db.connect()
    db.create_tables(
        [
            Class,
            Student,
            ClassRoster,
            Assignment,
            AssignmentQuestion,
            ClassAssignment,
            StudentAssignmentScore,
            StudentQuestionScore,
            AssignmentCategoryWeight,
        ]
    )


# -----------------------------------------------------
# Seeding functions
# -----------------------------------------------------
def seed_classes(n=10):
    """Create several classes with random dates."""
    print(f"Creating {n} classes...")

    classes = []
    for i in range(n):
        start = date(2024, 9, 1) + timedelta(days=randint(-20, 20))
        end = start + timedelta(days=randint(120, 200))
        classes.append(
            Class.create(
                name=fake.bs().title() + f" {randint(100, 499)}",
                start_date=start,
                end_date=end,
            )
        )
    return classes


def seed_students(n=50):
    print(f"Creating {n} students...")

    students = []
    for i in range(n):
        students.append(
            Student.create(
                student_number=f"S{1000+i}",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )
        )
    return students


def seed_rosters(classes, students):
    print("Enrolling students into classes...")

    rosters = []
    for class_ in classes:
        num_students = randint(15, 35)
        enrolled = fake.random_elements(students, length=num_students, unique=True)

        for student in enrolled:
            rosters.append(ClassRoster.create(class_ref=class_, student=student))
    return rosters


def seed_assignments_per_class(n=6):
    """
    Each class gets its own set of assignments:
    3 quizzes, 2 homework, 1 test (can be altered).
    """
    categories = ["quiz", "quiz", "quiz", "homework", "homework", "test"]

    assignments = []
    for i in range(n):
        title = f"Assignment {i+1}"
        assignments.append(Assignment.create(title=title, category=categories[i]))
    return assignments


def seed_questions(assignments):
    print("Creating assignment questions...")

    all_questions = []
    for assignment in assignments:
        q_count = randint(3, 6)
        for _ in range(q_count):
            all_questions.append(
                AssignmentQuestion.create(
                    assignment=assignment,
                    text=fake.sentence(),
                    point_value=uniform(3, 10),
                )
            )
    return all_questions


def seed_class_assignments(classes):
    print("Attaching assignments to each class...")

    class_assignments = []
    per_class = {}

    for class_ in classes:
        assignments = seed_assignments_per_class()
        per_class[class_] = assignments

        for assignment in assignments:
            class_assignments.append(
                ClassAssignment.create(class_ref=class_, assignment=assignment)
            )

    return class_assignments, per_class


def seed_category_weights(classes):
    print("Adding category weights...")

    weights = {"quiz": 0.3, "homework": 0.3, "test": 0.4}

    for class_ in classes:
        for cat, weight in weights.items():
            AssignmentCategoryWeight.create(
                class_ref=class_, category=cat, weight=weight
            )


def seed_scores(rosters, class_assignments, assignment_to_questions):
    print("Generating student scores...")

    # Build a mapping from assignment → list of questions
    assignment_map = {}
    for aq in assignment_to_questions:
        assignment_map.setdefault(aq.assignment, []).append(aq)

    # Build class → assignments
    class_assignment_map = {}
    for ca in class_assignments:
        class_assignment_map.setdefault(ca.class_ref, []).append(ca)

    # For each roster entry (student in class), assign scores
    for roster_entry in rosters:
        class_ = roster_entry.class_ref
        assignments = class_assignment_map[class_]

        for class_assignment in assignments:
            assignment = class_assignment.assignment
            questions = assignment_map[assignment]

            # Score assignment
            total = 0
            for q in questions:
                points = uniform(0, q.point_value)
                total += points

                StudentQuestionScore.create(
                    student=roster_entry.student,
                    assignment_question=q,
                    points_scored=round(points, 2),
                )

            StudentAssignmentScore.create(
                roster_entry=roster_entry,
                class_assignment=class_assignment,
                total_score=round(total, 2),
                total_time=randint(60, 1200),
            )


# -----------------------------------------------------
# Main orchestration
# -----------------------------------------------------
def main():
    reset_database()

    classes = seed_classes()
    students = seed_students()
    rosters = seed_rosters(classes, students)
    class_assignments, per_class_assignments = seed_class_assignments(classes)

    # Flatten all questions
    all_questions = []
    for assignment_list in per_class_assignments.values():
        all_questions.extend(seed_questions(assignment_list))

    seed_category_weights(classes)
    seed_scores(rosters, class_assignments, all_questions)

    print("Database seeded successfully with large data!")


if __name__ == "__main__":
    main()
