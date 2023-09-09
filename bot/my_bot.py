import telebot
from settings import Settings
from .bot_function_candidate import candidate_handler
from .bot_function_job_position import vacancy_handler
token = Settings.BOT_KEY
bot = telebot.TeleBot(token)

candidate_handler(bot)
vacancy_handler(bot)

# @bot.message_handler(commands=["start"])
# def start_message(message):
#     bot.reply_to(message, f'{message.from_user.id}')
