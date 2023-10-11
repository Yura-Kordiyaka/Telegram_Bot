from db.database_setings import db
from db.models import Candidates, Skills, JobPositions, Requirements, CandidateResume, Recruiters
from sqlalchemy import func, or_
from db.schemas_models import List, JobPositionsCreate, RequirementsCreate, \
 RecruiterCreate


def add_vacancy(vacancy_data: JobPositionsCreate, requirements: List[RequirementsCreate]):
    new_vacancy = JobPositions(**vacancy_data.dict())

    db.add(new_vacancy)
    db.commit()
    db.refresh(new_vacancy)

    for requirement in requirements:
        db_requirement = Requirements(**requirement.dict(), job_position_id=new_vacancy.id)
        db.add(db_requirement)

    db.commit()
    return new_vacancy


def get_all_candidates_by_requirements(job_position_id: int):
    job_position = db.query(JobPositions).get(job_position_id)

    required_skills = [requirement.name.lower() for requirement in job_position.requirements]

    candidates_with_matching_skills = (
        db.query(Candidates.id, CandidateResume.chat_id)
        .join(Skills, Candidates.id == Skills.candidate_id)
        .join(CandidateResume, Candidates.id == CandidateResume.candidate_id)
        .filter(
            or_(
                func.lower(Skills.name).in_(required_skills),
                func.lower(Candidates.main_skill).in_(required_skills),
                func.lower(Candidates.desired_job_position).like(func.lower(f"{job_position.title}"))
            )
        )
        .distinct(CandidateResume.chat_id)
        .all()
    )

    return candidates_with_matching_skills


def add_recruiter_vacancy(recruiter_add: RecruiterCreate):
    new_recruiter_resume_data = Recruiters(**recruiter_add.dict())
    db.add(new_recruiter_resume_data)
    db.commit()
    return new_recruiter_resume_data


def check_recruiter_time(chat_id):
    recent_recruiters = (
        db.query(Recruiters)
        .filter(Recruiters.chat_id == chat_id)
        .order_by(Recruiters.created_at)
        .limit(3)
        .all()
    )
    recent_recruiters_dicts = [recruiter.to_dict() for recruiter in recent_recruiters]
    return recent_recruiters_dicts
