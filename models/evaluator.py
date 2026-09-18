import enum

from sqlalchemy import Boolean, Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class EvaluatorType(enum.Enum):
    TRE = "TRE"
    SIM = "SIM"
    LTC = "LTC"
    CHIEF = "Chief Pilot"
    MANAGER = "Training Manager"


class Evaluator(Base):
    __tablename__ = "evaluators"

    evaluator_id = Column(Integer, primary_key=True)
    evaluator_code = Column(String(32), unique=True, nullable=False)
    name = Column(String(128), nullable=False)
    evaluator_type = Column(Enum(EvaluatorType), nullable=False)
    aircraft_type = Column(String(32), nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    assessment_sessions = relationship("AssessmentSession", back_populates="evaluator")
