from models.base import SessionLocal
from models.competency import Competency, ObservableBehavior
from services.database import init_db


def test_database_initializes_and_loads_competencies():
    init_db()
    session = SessionLocal()
    try:
        assert session.query(Competency).count() == 9
        assert session.query(ObservableBehavior).count() >= 45
    finally:
        session.close()
