from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from .base import Base


class Threat(Base):
    __tablename__ = "threats"

    threat_id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.event_id", ondelete="CASCADE"), nullable=False)
    threat_description = Column(Text, nullable=False)
    threat_type = Column(String(64), nullable=False)

    event = relationship("Event", back_populates="threats")


class Error(Base):
    __tablename__ = "errors"

    error_id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.event_id", ondelete="CASCADE"), nullable=False)
    error_description = Column(Text, nullable=False)
    error_type = Column(String(64), nullable=False)

    event = relationship("Event", back_populates="errors")


class UndesiredAircraftState(Base):
    __tablename__ = "undesired_aircraft_states"

    uas_id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.event_id", ondelete="CASCADE"), nullable=False)
    state_description = Column(Text, nullable=False)
    state_type = Column(String(64), nullable=False)

    event = relationship("Event", back_populates="undesired_states")


class Countermeasure(Base):
    __tablename__ = "countermeasures"

    countermeasure_id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.event_id", ondelete="CASCADE"), nullable=False)
    countermeasure_description = Column(Text, nullable=False)
    countermeasure_type = Column(String(64), nullable=False)
    competency_involved = Column(String(16), nullable=True)
    effectiveness = Column(String(32), nullable=True)

    event = relationship("Event", back_populates="countermeasures")
