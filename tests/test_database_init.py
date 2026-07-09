from gradebook.database import models
from gradebook.database.models import db


def test_ensure_db_initialized_initializes_uninitialized_proxy(tmp_path):
    db.initialize(None)

    models.ensure_db_initialized(db_path=str(tmp_path / "gradebook.db"), create_tables=True)

    assert db.obj is not None
