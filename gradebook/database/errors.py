import typing

if typing.TYPE_CHECKING:
    from gradebook.database.models import BaseModel


class RecordNotFoundError(Exception):
    """Exception raised when a database record is not found."""
    def __init__(self, id: int, type: "BaseModel") -> None:
        super().__init__(f"No {type.__name__} record with ID {id} found.")