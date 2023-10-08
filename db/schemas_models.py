from pydantic import BaseModel, validator
from typing import List
from datetime import datetime


class CandidatesBase(BaseModel):
    desired_job_position: str
    email: str
    first_name: str
    last_name: str
    main_skill: str
    experience: str
    desired_salary: int


class CandidatesCreate(CandidatesBase):
    pass


class Candidates(CandidatesBase):
    id: int
    skills: List["Skills"] = []

    class Config:
        orm_mode = True


class SkillsBase(BaseModel):
    name: str


class SkillsCreate(SkillsBase):
    pass


class Skills(SkillsBase):
    id: int
    candidate_id: int

    class Config:
        orm_mode = True


class JobPositionsBase(BaseModel):
    title: str
    description: str
    salary: int


class JobPositionsCreate(JobPositionsBase):
    pass


class JobPositions(JobPositionsBase):
    id: int
    requirements: List["Requirements"] = []

    class Config:
        orm_mode = True


class RequirementsBase(BaseModel):
    name: str


class RequirementsCreate(RequirementsBase):
    pass


class Requirements(RequirementsBase):
    id: int
    job_position_id: int

    class Config:
        orm_mode = True


class ApplicationsBase(BaseModel):
    job_position_id: int
    candidate_id: int
    status: str


class ApplicationsCreate(ApplicationsBase):
    pass


class Applications(ApplicationsBase):
    id: int

    class Config:
        orm_mode = True


class CandidateResumeBase(BaseModel):
    candidate_id: int
    chat_id: int


class CandidateResumeCreate(CandidateResumeBase):
    pass


class CandidateResumes(CandidateResumeBase):
    id: int
    create_at: datetime

    class Config:
        orm_mode = True
