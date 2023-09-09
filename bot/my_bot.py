import telebot
from settings import Settings
from telebot import types
from utilits import add_candidate
from sqlalchemy.orm import Session
from database_setings import get_database_session
from fastapi import Depends
import requests
from schemas_models import *
from .bot_function_candidate import candidate_handler

token = Settings.BOT_KEY
bot = telebot.TeleBot(token)

candidate_handler(bot)


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.reply_to(message, f'{message.from_user.id}')
