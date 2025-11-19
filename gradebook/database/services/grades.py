"""
Category weighting and final grade calculation.
"""

from __future__ import annotations
from typing import Dict
from models import (
    AssignmentCategoryWeight,
    Class,
    StudentCategoryScore,
    AssignmentType,
    ClassRoster
)


from peewee import DoesNotExist

def set_category_weight(cls: Class, category_type: str, weight: float) -> AssignmentCategoryWeight:
    """
    Set the weight for a category in a class.
    If a record exists, update it; otherwise create it.
    """
    from models import AssignmentCategoryWeight

    try:
        cat_weight = AssignmentCategoryWeight.get(
            AssignmentCategoryWeight.class_ref == cls,
            AssignmentCategoryWeight.type == category_type
        )
        cat_weight.weight = weight
        cat_weight.save()
    except DoesNotExist:
        cat_weight = AssignmentCategoryWeight.create(
            class_ref=cls,
            type=category_type,
            weight=weight  # ✅ must provide this!
        )
    return cat_weight



def compute_student_category_totals(roster_entry: ClassRoster) -> Dict[str, float]:
    """Compute total points for each assignment category."""
    totals = {t.value: 0.0 for t in AssignmentType}

    for sa in roster_entry.assignments:
        a_type = sa.class_assignment.assignment.type
        totals[a_type] += sa.total_score or 0

    return totals


def store_student_category_totals(roster_entry: ClassRoster) -> Dict[str, StudentCategoryScore]:
    """Store computed category totals into the database."""
    totals = compute_student_category_totals(roster_entry)
    out = {}

    for a_type, total in totals.items():
        scs, _ = StudentCategoryScore.get_or_create(
            roster_entry=roster_entry,
            type=a_type
        )
        scs.total_score = total
        scs.save()
        out[a_type] = scs

    return out


def compute_weighted_grade(roster_entry: ClassRoster) -> float:
    """Compute the final weighted grade for a student."""
    category_totals = compute_student_category_totals(roster_entry)

    weights = {
        w.type: w.weight
        for w in roster_entry.class_ref.category_weights
    }

    grade = sum(category_totals[a_type] * weights.get(a_type, 0.0) for a_type in category_totals)
    return grade
