import os

import requests
from dotenv import load_dotenv

load_dotenv()


class Settings:
    BOT_KEY = os.getenv('BOT_API_KEY')
    ADMIN = os.getenv('ADMIN_CHAT_ID')
    NGROK_URL = os.getenv('NGROK_URL')
    DATABASE_CONNECTION = os.getenv('DATABASE_CONNECTION')
