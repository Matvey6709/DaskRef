import os

from aiogram import Bot
from os import getenv

from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
count_ref = 14
curs = 7
chat_id = [f'@{os.getenv("URL_TG")}']
chat_url = [f'https://t.me/{os.getenv("URL_TG")}']
