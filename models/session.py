import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import Base


class AssessmentType(enum.Enum):
    SIMULATOR = "Simulator"
    EBT = "EBT"
    LINE_CHECK = "Line Check"
    RECURRENT = "Recurrent Training"
    TRAINING_SCENARIO = "Training Scenario"


class PhaseOfFlight(enum.Enum):
    PRE_FLIGHT = "Pre-flight"
    TAKEOFF = "Takeoff"
    CLIMB = "Climb"
    CRUISE = "Cruise"
    DESCENT = "Descent"
    APPROACH = "Approach"
    LANDING = "Landing"
    POST_FLIGHT = "Post-flight"


class PFPMRole(enum.Enum):
    PF = "PF"
    PM = "PM"


class AssessmentSession(Base):
    __tablename__ = "assessment_sessions"

    session_id = Column(Integer, primary_key=True)
    pilot_id = Column(Integer, ForeignKey("pilots.pilot_id", ondelete="CASCADE"), nullable=False)
    evaluator_id = Column(Integer, ForeignKey("evaluators.evaluator_id", ondelete="CASCADE"), nullable=False)
    assessment_type = Column(Enum(AssessmentType), nullable=False)
    aircraft_type = Column(String(32), nullable=False)
    fleet = Column(String(64), nullable=False)
    assessment_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    training_module = Column(String(128), nullable=False)
    scenario_event = Column(String(128), nullable=False)
    pf_pm_role = Column(Enum(PFPMRole), nullable=False)
    phase_of_flight = Column(Enum(PhaseOfFlight), nullable=False)
    comments = Column(Text, nullable=True)

    pilot = relationship("Pilot", back_populates="assessment_sessions")
    evaluator = relationship("Evaluator", back_populates="assessment_sessions")
    events = relationship("Event", back_populates="session")
    competency_assessments = relationship("CompetencyAssessment", back_populates="session")
    observations = relationship("Observation", back_populates="session")


class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("assessment_sessions.session_id", ondelete="CASCADE"), nullable=False)
    event_description = Column(Text, nullable=False)
    phase_of_flight = Column(Enum(PhaseOfFlight), nullable=False)

    session = relationship("AssessmentSession", back_populates="events")
    threats = relationship("Threat", back_populates="event")
    errors = relationship("Error", back_populates="event")
    undesired_aircraft_states = relationship("UndesiredAircraftState", back_populates="event")
    countermeasures = relationship("Countermeasure", back_populates="event")
