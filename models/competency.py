import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import Base


class CompetencyCode(enum.Enum):
    KNO = "KNO"
    PRO = "PRO"
    COM = "COM"
    FPA = "FPA"
    FPM = "FPM"
    LTW = "LTW"
    PSD = "PSD"
    SAW = "SAW"
    WLM = "WLM"


class Competency(Base):
    __tablename__ = "competencies"

    competency_id = Column(Integer, primary_key=True)
    code = Column(Enum(CompetencyCode), unique=True, nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=False)

    observable_behaviors = relationship(
        "ObservableBehavior",
        back_populates="competency",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    assessments = relationship(
        "CompetencyAssessment",
        back_populates="competency",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class ObservableBehavior(Base):
    __tablename__ = "observable_behaviors"

    observable_behavior_id = Column(Integer, primary_key=True)
    competency_id = Column(Integer, ForeignKey("competencies.competency_id", ondelete="CASCADE"), nullable=False)
    description = Column(Text, nullable=False)

    competency = relationship("Competency", back_populates="observable_behaviors")
