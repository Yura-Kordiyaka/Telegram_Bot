from db.database_setings import db
from db.models import Candidates, Skills, JobPositions, Requirements, CandidateResume

from db.schemas_models import CandidatesCreate, SkillsCreate, List, JobPositionsCreate, RequirementsCreate, \
    CandidateResumeCreate


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


def add_candidate_resume(candidate_resume_data: CandidateResumeCreate):
    new_candidate_resume_data = CandidateResume(**candidate_resume_data.dict())
    db.add(new_candidate_resume_data)
    db.commit()
    return new_candidate_resume_data


def get_candidate_resume(chat_id):
    candidate_resume = db.query(CandidateResume).filter(CandidateResume.chat_id == chat_id).first()
    if candidate_resume:
        return candidate_resume.candidate.to_dict_with_skills()
    else:
        return False


def get_candidates_with_skills(id):
    candidate = db.query(Candidates).filter(Candidates.id == id).first()
    if candidate:
        return candidate.to_dict_with_skills()


def add_vacancy(vacancy_data: JobPositionsCreate, requirements: List[RequirementsCreate]):
    new_job_position = JobPositions(**vacancy_data.dict())

    db.add(new_job_position)
    db.commit()
    db.refresh(new_job_position)

    for requirement in requirements:
        db_requirement = Requirements(**requirement.dict(), job_position_id=new_job_position.id)
        db.add(db_requirement)

    db.commit()
    return new_job_position
