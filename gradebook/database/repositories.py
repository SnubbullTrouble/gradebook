from peewee import prefetch
from .models import (
    Assignment,
    AssignmentQuestion,
    Class,
    ClassAssignment,
)


def get_class_by_id(class_id: int):
    """Return Class or None for the given id."""
    return Class.get_or_none(Class.id == class_id)


def fetch_assignments_for_class(class_id: int, category: str | None = None):
    base_q = (
        Assignment.select()
        .join(ClassAssignment)
        .join(Class)
        .where(Class.id == class_id)
    )
    if category:
        base_q = base_q.where(Assignment.category == category)

    return list(prefetch(base_q, AssignmentQuestion))
