from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database_setings import Base

class Candidates(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True)
    email = Column(String(250), unique=True, nullable=False)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    experience = Column(String(150), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    desired_salary = Column(Integer, nullable=False)

    skills = relationship("Skills", back_populates='candidate')


class Skills(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)

    candidate = relationship("Candidates", back_populates='skills')
    candidate_id = Column(Integer, ForeignKey('candidates.id'))


class JobPositions(Base):
    __tablename__ = "job_positions"
    id = Column(Integer, primary_key=True)
    title = Column(String(300))
    description = Column(Text)

    requirements = relationship("Requirements", back_populates='job_position')


class Requirements(Base):
    __tablename__ = "requirements"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    job_position = relationship("JobPositions", back_populates='requirements')
    job_position_id = Column(Integer, ForeignKey('job_positions.id'))

class Applications(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True)
    job_position_id = Column(Integer, ForeignKey('job_positions.id'))
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    status = Column(String(250), nullable=False)
