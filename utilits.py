from database_setings import db
from models import Candidates, Skills

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


def get_all_candidates_with_skills():
    candidate = db.query(Candidates).filter(Candidates.id == 19).first()
    candidates_with_skills = []

    candidate_data = {
        'id': candidate.id,
        'name': candidate.first_name,
        'skills': []
    }

    for skill in candidate.skills:
        skill_data = {
            'id': skill.id,
            'skill_name': skill.name,
        }
        candidate_data['skills'].append(skill_data)

    candidates_with_skills.append(candidate_data)

    return candidates_with_skills
