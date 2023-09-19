import telebot
from settings import Settings
from bot.bot_function.bot_function_candidate import candidate_handler
from bot.bot_function.bot_function_job_position import vacancy_handler
# from .bot_menu import menu_handler
token = Settings.BOT_KEY
bot = telebot.TeleBot(token)

candidate_handler(bot)
vacancy_handler(bot)
# menu_handler(bot)

