import dataclasses
from typing import List
from peewee import IntegrityError
from gradebook.database.models import Assignment, AssignmentQuestion, ClassAssignment, Class

@dataclasses.dataclass
class Question:
    question: str
    points: int

def create_assignment(title: str, category: str, questions: List[Question]) -> Assignment:
    """
    Create an assignment with multiple questions.

    Args:
        title: Assignment title.
        category: "quiz", "test", or "homework".
        question_points: List of point values for each question.

    Returns:
        Assignment: The created Assignment object.
    """
    assignment = Assignment.create(title=title, category=category)
    for q in questions:
        AssignmentQuestion.create(
            assignment=assignment,
            text=q.question,
            point_value=q.points
        )
    return assignment

def assign_to_class(cls: "Class", assignment: Assignment) -> ClassAssignment:
    """
    Assign an assignment template to a class.

    Duplicate assignments for the same class should raise IntegrityError.

    Args:
        cls (Class): The class to assign the assignment to.
        assignment (Assignment): The assignment template.

    Returns:
        ClassAssignment: The created class-assignment record.

    Raises:
        IntegrityError: If the assignment is already linked to the class.
    """
    total_points = sum(q.point_value for q in assignment.questions)

    # This will raise IntegrityError if the class_ref/assignment combination already exists.
    return ClassAssignment.create(
        class_ref=cls,
        assignment=assignment,
        total_points=total_points
    )

def get_assignments_for_class(class_id: int, category: str = None) -> list[Assignment]:
    if category:
        return list(Assignment.select().join(ClassAssignment).join(Class).where(Class.id == class_id and Assignment.category == category))
    else:
        return list(Assignment.select().join(ClassAssignment).join(Class).where(Class.id == class_id))

#def get_student_assignment_scores(student: "Student", assignment_type: str) -> list[Assignment]:

