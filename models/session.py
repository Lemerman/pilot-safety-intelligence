import enum
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from .base import Base


class AssessmentType(str, enum.Enum):
    SIMULATOR = "Simulator"
    EBT = "EBT"
    LINE_CHECK = "Line Check"
    RECURRENT = "Recurrent Training"
    TRAINING_SCENARIO = "Training Scenario"


class PhaseOfFlight(str, enum.Enum):
    PRE_FLIGHT = "Pre-flight"
    TAKEOFF = "Takeoff"
    CLIMB = "Climb"
    CRUISE = "Cruise"
    DESCENT = "Descent"
    APPROACH = "Approach"
    LANDING = "Landing"
    POST_FLIGHT = "Post-flight"


class PFPMRole(str, enum.Enum):
    PF = "PF"
    PM = "PM"


class AssessmentSession(Base):
    __tablename__ = "assessment_sessions"

    session_id = Column(Integer, primary_key=True, index=True)
    pilot_id = Column(Integer, ForeignKey("pilots.pilot_id", ondelete="CASCADE"), nullable=False)
    evaluator_id = Column(Integer, ForeignKey("evaluators.evaluator_id", ondelete="CASCADE"), nullable=False)
    assessment_type = Column(Enum(AssessmentType), nullable=False)
    aircraft_type = Column(String(32), nullable=False)
    fleet = Column(String(64), nullable=False)
    assessment_date = Column(DateTime, nullable=False)
    training_module = Column(String(128), nullable=True)
    scenario_event = Column(String(128), nullable=True)
    pf_pm_role = Column(Enum(PFPMRole), nullable=False)
    phase_of_flight = Column(Enum(PhaseOfFlight), nullable=False)
    comments = Column(Text, nullable=True)

    pilot = relationship("Pilot", back_populates="sessions")
    evaluator = relationship("Evaluator", back_populates="sessions")
    events = relationship("Event", back_populates="session", cascade="all, delete-orphan")
    competency_assessments = relationship("CompetencyAssessment", back_populates="session", cascade="all, delete-orphan")


class Event(Base):
    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("assessment_sessions.session_id", ondelete="CASCADE"), nullable=False)
    event_description = Column(Text, nullable=False)
    phase_of_flight = Column(Enum(PhaseOfFlight), nullable=False)

    session = relationship("AssessmentSession", back_populates="events")
    threats = relationship("Threat", back_populates="event", cascade="all, delete-orphan")
    errors = relationship("Error", back_populates="event", cascade="all, delete-orphan")
    undesired_states = relationship("UndesiredAircraftState", back_populates="event", cascade="all, delete-orphan")
    countermeasures = relationship("Countermeasure", back_populates="event", cascade="all, delete-orphan")
    observations = relationship("Observation", back_populates="event", cascade="all, delete-orphan")
    safety_occurrences = relationship("SafetyOccurrence", back_populates="event", cascade="all, delete-orphan")
