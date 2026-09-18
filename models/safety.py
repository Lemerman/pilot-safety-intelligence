from sqlalchemy import Column, DateTime, Integer, String, Text

from .base import Base, utcnow_naive


class SafetyOccurrence(Base):
    __tablename__ = "safety_occurrences"

    occurrence_id = Column(Integer, primary_key=True)
    occurrence_class = Column(String(64), nullable=False)
    occurrence_category = Column(String(64), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=utcnow_naive)
