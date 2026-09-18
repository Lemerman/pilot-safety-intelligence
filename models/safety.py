from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from .base import Base


class SafetyOccurrence(Base):
    __tablename__ = "safety_occurrences"

    occurrence_id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.event_id", ondelete="CASCADE"), nullable=False)
    occurrence_class = Column(String(64), nullable=True)
    occurrence_category = Column(String(64), nullable=True)
    description = Column(Text, nullable=True)

    event = relationship("Event", back_populates="safety_occurrences")
