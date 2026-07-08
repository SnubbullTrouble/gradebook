from gradebook.database.services.students import create_student_dto, get_student_dto
from gradebook.database.dtos import StudentDTO


def test_create_student_dto_returns_dto():
    dto = create_student_dto("DTO1", "DT", "O")
    assert isinstance(dto, StudentDTO)
    assert dto.student_number == "DTO1"


def test_get_student_dto_not_found_returns_none():
    res = get_student_dto("NO_SUCH_DTO")
    assert res is None
