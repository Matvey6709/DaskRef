from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

main_reply = ReplyKeyboardBuilder()
main_reply.add(KeyboardButton(text="💎 Заработать"))
main_reply.add(KeyboardButton(text="💼 Кабинет"))
main_reply.add(KeyboardButton(text="📋 Информация"))
main_reply.adjust(2)