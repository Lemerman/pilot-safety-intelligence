import enum
from sqlalchemy import Boolean, Column, Enum, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class EvaluatorType(str, enum.Enum):
    TRE = "TRE"
    SIM = "SIM"
    LTC = "LTC"
    CHIEF = "CHIEF"
    MANAGER = "MANAGER"


class Evaluator(Base):
    __tablename__ = "evaluators"

    evaluator_id = Column(Integer, primary_key=True, index=True)
    evaluator_code = Column(String(32), unique=True, nullable=False, index=True)
    name = Column(String(128), nullable=False)
    evaluator_type = Column(Enum(EvaluatorType), nullable=False)
    aircraft_type = Column(String(32), nullable=False)
    active = Column(Boolean, default=True, nullable=False)

    sessions = relationship("AssessmentSession", back_populates="evaluator", cascade="all, delete-orphan")
