from fastapi import FastAPI, Request, Depends,HTTPException
from settings import Settings
import uvicorn
from bot.my_bot import bot
import telebot
from schemas import CandidateCreate
from database_setings import engine, get_database_session
import models
from models import Candidates, Skills
from sqlalchemy.orm import Session
# from utilits import add_candidate

app = FastAPI()
ngrok_url = Settings.NGROK_URL

models.Base.metadata.create_all(bind=engine)


@app.post("/add_candidate/")
async def add_candidate(candidate_data: CandidateCreate, session: Session = Depends(get_database_session)):
    try:
        new_candidate = Candidates(
            email=candidate_data.email,
            first_name=candidate_data.first_name,
            last_name=candidate_data.last_name,
            experience=candidate_data.experience,
            desired_salary=candidate_data.desired_salary
        )

        session.add(new_candidate)
        session.commit()

        return new_candidate
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Помилка при додаванні кандидата: {e}')

@app.post("/add_skill/")
async def add_skill(candidate_id: int, skill_data: dict, session: Session = Depends(get_database_session)):
    # Отримання кандидата за його ID
    candidate = session.query(Candidates).filter_by(id=candidate_id).first()

    # Отримання назви навички з запиту
    skill_name = skill_data['name']

    # Створення нової навички та додавання її до кандидата
    new_skill = Skills(name=skill_name)
    candidate.skills.append(new_skill)

    # Збереження змін у базі даних
    session.commit()

    return new_skill


@app.get("/candidates/skills")
async def get_candidate_skills(candidate_id: int, session: Session = Depends(get_database_session)):
    # Знаходимо кандидата за його ID
    candidate = session.query(Candidates).filter_by(id=candidate_id).first()

    # Отримуємо список навичок кандидата
    skills = candidate.skills

    # Повертаємо список навичок як відповідь
    return {"skills": [skill.name for skill in skills]}


@app.post("/")
async def handle_webhook(request: Request):
    update = await request.json()
    # obj = Answer(**update)
    # print(update)
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    return {"ok": True}


if __name__ == "__main__":
    public = ngrok_url
    bot.set_webhook(f"{public}/")
    uvicorn.run("main:app", host='0.0.0.0', port=8000,
                reload=True)
