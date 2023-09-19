from fastapi import FastAPI, Request
from settings import Settings
import uvicorn
from bot.my_bot import bot
import telebot
from db.database_setings import engine
from db import models

# from utilits import add_candidate

app = FastAPI()
ngrok_url = Settings.NGROK_URL

models.Base.metadata.create_all(bind=engine)


@app.post("/")
async def handle_webhook(request: Request):
    update = await request.json()
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    return {"ok": True}


if __name__ == "__main__":
    public = ngrok_url
    bot.set_webhook(f"{public}/")
    uvicorn.run("main:app", host='0.0.0.0', port=8000,
                reload=True)
