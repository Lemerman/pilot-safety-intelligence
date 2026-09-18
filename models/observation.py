import enum
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import Base


class ObservationType(enum.Enum):
    POSITIVE = "Positive"
    DEVELOPMENT = "Development"
    SAFETY = "Safety"


class Observation(Base):
    __tablename__ = "observations"

    observation_id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("assessment_sessions.session_id", ondelete="CASCADE"), nullable=False)
    observation_type = Column(String(32), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    session = relationship("AssessmentSession", back_populates="observations")


class CompetencyAssessment(Base):
    __tablename__ = "competency_assessments"

    competency_assessment_id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("assessment_sessions.session_id", ondelete="CASCADE"), nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.competency_id", ondelete="CASCADE"), nullable=False)
    how_many = Column(String(32), nullable=False)
    how_often = Column(String(64), nullable=False)
    tem_outcome = Column(String(64), nullable=False)
    grade = Column(Integer, nullable=True)
    grade_not_observed = Column(Boolean, nullable=False, default=False)
    evaluator_justification = Column(Text, nullable=False)

    session = relationship("AssessmentSession", back_populates="competency_assessments")
    competency = relationship("Competency", back_populates="assessments")


class PilotCompetencyProfile(Base):
    __tablename__ = "pilot_competency_profiles"

    profile_id = Column(Integer, primary_key=True)
    pilot_id = Column(Integer, ForeignKey("pilots.pilot_id", ondelete="CASCADE"), nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.competency_id", ondelete="CASCADE"), nullable=False)
    current_grade = Column(Integer, nullable=True)
    grade_not_observed = Column(Boolean, nullable=False, default=False)
    last_assessed_at = Column(DateTime, nullable=True)

    pilot = relationship("Pilot", back_populates="competency_profiles")
    competency = relationship("Competency")
