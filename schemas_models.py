from pydantic import BaseModel, validator
from typing import List
from datetime import datetime


class CandidatesBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    experience: str
    desired_salary: int


class CandidatesCreate(CandidatesBase):
    pass

    @validator('desired_salary')
    def validate_desired_salary(cls, value):
        if value <= 0:
            raise ValueError()
        return value


class Candidates(CandidatesBase):
    id: int
    created_at: datetime
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
