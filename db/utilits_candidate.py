from db.database_setings import db
from db.models import Candidates, Skills, CandidateResume
from sqlalchemy import func, and_, or_
from db.schemas_models import CandidatesCreate, SkillsCreate, List,  \
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


def get_candidate_with_skills(id):
    candidate = db.query(Candidates).filter(Candidates.id == id).first()
    if candidate:
        return candidate.to_dict_with_skills()





def search_candidates_by_language_and_level(programming_language, experience_level):
    candidates = (
        db.query(Candidates)
        .join(Skills, Candidates.id == Skills.candidate_id)
        .filter(
            or_(
                and_(
                    func.lower(Skills.name) == func.lower(programming_language),
                    func.lower(Candidates.desired_job_position).like(func.lower(f"%{experience_level}%"))
                ),
                and_(
                    func.lower(Candidates.main_skill) == func.lower(programming_language),
                    func.lower(Candidates.desired_job_position).like(func.lower(f"%{experience_level}%"))
                )
            )
        )
        .order_by(
            func.lower(Candidates.main_skill) != func.lower(programming_language),
        )
        .all()
    )

    candidates_data = []
    for candidate in candidates:
        candidate_data = candidate.to_dict_with_skills()
        candidates_data.append(candidate_data)

    return candidates_data


def search_candidates_by_skill(skill_name):
    candidates = db.query(Candidates).join(Skills).filter(Skills.name == skill_name).all()
    candidates_data = []
    for candidate in candidates:
        candidate_data = candidate.to_dict_with_skills()
        candidates_data.append(candidate_data)
    return candidates_data
