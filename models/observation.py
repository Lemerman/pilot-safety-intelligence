import enum
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from .base import Base


class ObservationType(str, enum.Enum):
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"


class Observation(Base):
    __tablename__ = "observations"

    observation_id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.event_id", ondelete="CASCADE"), nullable=False)
    observation_type = Column(String(16), nullable=True)
    description = Column(Text, nullable=True)

    event = relationship("Event", back_populates="observations")


class CompetencyAssessment(Base):
    __tablename__ = "competency_assessments"

    competency_assessment_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("assessment_sessions.session_id", ondelete="CASCADE"), nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.competency_id", ondelete="CASCADE"), nullable=False)
    how_many = Column(String(32), nullable=True)
    how_often = Column(String(64), nullable=True)
    tem_outcome = Column(String(64), nullable=True)
    grade = Column(Integer, nullable=True)
    grade_not_observed = Column(Boolean, default=False, nullable=False)
    evaluator_justification = Column(Text, nullable=True)

    session = relationship("AssessmentSession", back_populates="competency_assessments")
    competency = relationship("Competency", back_populates="competency_assessments")


class PilotCompetencyProfile(Base):
    __tablename__ = "pilot_competency_profiles"

    profile_id = Column(Integer, primary_key=True, index=True)
    pilot_id = Column(Integer, ForeignKey("pilots.pilot_id", ondelete="CASCADE"), nullable=False)
    competency_id = Column(Integer, ForeignKey("competencies.competency_id", ondelete="CASCADE"), nullable=False)
    profile_notes = Column(Text, nullable=True)
