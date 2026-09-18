from models.base import SessionLocal
from models import Pilot, Evaluator, AssessmentSession, CompetencyAssessment
from services.database import init_db
from services.demo_data import generate_demo_data


def test_demo_data_generation_counts():
    init_db()
    generate_demo_data()

    session = SessionLocal()
    try:
        assert session.query(Pilot).count() == 20
        assert session.query(Evaluator).count() == 5
        assert session.query(AssessmentSession).count() == 100
        assert session.query(CompetencyAssessment).count() > 0
    finally:
        session.close()
