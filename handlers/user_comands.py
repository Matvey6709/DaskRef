import os

from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from dotenv import load_dotenv

from database.requests import set_user, set_test, set_test2
from keyboards.inline import builderAdmin
from keyboards.reply import main_reply

router = Router()
load_dotenv()

@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject):
    await set_user(message.from_user.id, command)

    await message.answer("Привет! Я бот, который платит за подписки на каналы",
                         reply_markup=main_reply.as_markup(resize_keyboard=True))
    if message.from_user.id == os.getenv('ADMIN_ID'):
        await message.answer(
            "Eсли ты видишь это сообщение, значит ты входишь в круг лиц, которые могут использовать админ панель",
            reply_markup=builderAdmin.as_markup(resize_keyboard=True))
