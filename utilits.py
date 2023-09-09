from fastapi import FastAPI, Request, Depends
from database_setings import engine, db
from models import Candidates, Skills
from sqlalchemy.orm import Session
from schemas_models import CandidatesCreate, SkillsCreate, List


def add_candidate(candidate_data: CandidatesCreate, skills: List[SkillsCreate]):
    new_candidate = Candidates(**candidate_data.dict())

    db.add(new_candidate)
    db.commit()
    db.refresh(new_candidate)

    for skill in skills:
        db_skill = Skills(**skill.dict(), candidate_id=new_candidate.id)
        db.add(db_skill)

    db.commit()
    return new_candidate
