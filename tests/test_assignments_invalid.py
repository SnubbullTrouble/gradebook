import pytest
from gradebook.database.services.assignments import create_assignment


def test_create_assignment_invalid_category_raises():
    with pytest.raises(ValueError):
        create_assignment("Bad", "not_a_category", [5])
