from gradebook.database.services.assignments import (
    get_category_weight_dto,
    get_category_weights_for_class_dto,
)
from gradebook.database.services.classes import create_class
from gradebook.database.services.scoring import set_category_weight


def test_get_category_weight_dto_returns_none_when_missing():
    assert get_category_weight_dto(-1, "quiz") is None


def test_get_category_weight_dto_after_setting():
    c = create_class("Weight DTO")
    set_category_weight(c, "quiz", 0.5)
    dto = get_category_weight_dto(c.id, "quiz")
    assert dto is not None
    assert dto.category == "quiz"
    assert dto.weight == 0.5


def test_get_category_weights_for_class_dto_returns_list():
    c = create_class("Weight DTO List")
    set_category_weight(c, "quiz", 0.6)
    set_category_weight(c, "homework", 0.4)
    dtos = get_category_weights_for_class_dto(c.id)
    assert len(dtos) == 2
    assert {d.category for d in dtos} == {"quiz", "homework"}
