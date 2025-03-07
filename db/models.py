from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database_setings import Base


class Candidates(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True)
    email = Column(String(250), unique=True, nullable=False)
    first_name = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    main_skill = Column(String(150), nullable=False)
    experience = Column(String(150), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    desired_salary = Column(Integer, nullable=False)

    skills = relationship("Skills", back_populates='candidate', cascade="all, delete-orphan")
    candidate_resume = relationship("CandidateResume", back_populates='candidate', cascade="all, delete-orphan")
    desired_job_position = Column(String(300), nullable=False)

    def to_dict_with_skills(self):
        candidate_data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'main_skill': self.main_skill,
            'salary': self.desired_salary,
            'experience': self.experience,
            'desired_job_position': self.desired_job_position,
            'skills': [],
        }

        for skill in self.skills:
            skill_data = {
                'id': skill.id,
                'skill_name': skill.name,
            }
            candidate_data['skills'].append(skill_data)
        return candidate_data


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
    created_at = Column(DateTime, default=datetime.utcnow)
    salary = Column(Integer, nullable=False)
    recruiters_vacancy = relationship("Recruiters", back_populates='job_position', cascade="all, delete-orphan")
    requirements = relationship("Requirements", back_populates='job_position', cascade="all, delete-orphan")

    def to_dict_with_skills(self):
        job_position = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'salary': self.salary,
            'requirements': [],
        }

        for requirement in self.requirements:
            requirement_data = {
                'id': requirement.id,
                'requirement': requirement.name,
            }
            job_position['requirements'].append(requirement_data)
        return job_position


class Requirements(Base):
    __tablename__ = "requirements"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    job_position = relationship("JobPositions", back_populates='requirements')
    job_position_id = Column(Integer, ForeignKey('job_positions.id'))


class CandidateResume(Base):
    __tablename__ = "candidate_resume"
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    chat_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    candidate = relationship("Candidates", back_populates='candidate_resume')


class Recruiters(Base):
    __tablename__ = "recruiters_vacancy"
    id = Column(Integer, primary_key=True)
    job_position = relationship("JobPositions", back_populates='recruiters_vacancy')
    job_position_id = Column(Integer, ForeignKey('job_positions.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    chat_id = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "job_position_id": self.job_position_id,
            "created_at": self.created_at,
            "chat_id": self.chat_id,
        }