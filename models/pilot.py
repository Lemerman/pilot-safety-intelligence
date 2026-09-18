import enum

from sqlalchemy import Boolean, Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class PilotRole(enum.Enum):
    CAPTAIN = "Captain"
    FIRST_OFFICER = "First Officer"


class Pilot(Base):
    __tablename__ = "pilots"

    pilot_id = Column(Integer, primary_key=True)
    pilot_code = Column(String(32), unique=True, nullable=False)
    role = Column(Enum(PilotRole), nullable=False)
    aircraft_type = Column(String(32), nullable=False)
    fleet = Column(String(64), nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    assessment_sessions = relationship("AssessmentSession", back_populates="pilot")
    competency_profiles = relationship("PilotCompetencyProfile", back_populates="pilot")
