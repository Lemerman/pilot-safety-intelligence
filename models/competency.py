import enum
from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from .base import Base


class CompetencyCode(str, enum.Enum):
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

    competency_id = Column(Integer, primary_key=True, index=True)
    code = Column(Enum(CompetencyCode), unique=True, nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=False)

    observable_behaviors = relationship("ObservableBehavior", back_populates="competency", cascade="all, delete-orphan")
    competency_assessments = relationship("CompetencyAssessment", back_populates="competency", cascade="all, delete-orphan")


class ObservableBehavior(Base):
    __tablename__ = "observable_behaviors"

    behavior_id = Column(Integer, primary_key=True, index=True)
    competency_id = Column(Integer, ForeignKey("competencies.competency_id", ondelete="CASCADE"), nullable=False)
    description = Column(Text, nullable=False)

    competency = relationship("Competency", back_populates="observable_behaviors")
