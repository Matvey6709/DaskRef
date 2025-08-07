import asyncio
import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F

from callback import callbacks
from database.models import async_main
from handlers import bot_messages, user_comands
from utils import variables
from utils.middlewares import AntiFloodMiddleware


async def main():
    await async_main()
    logging.basicConfig(level=logging.INFO)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp["dp"] = dp
    dp["storage"] = storage

    dp.message.filter(F.chat.type == "private")
    dp.include_routers(user_comands.router, bot_messages.router, callbacks.router)
    dp.message.middleware(AntiFloodMiddleware())
    await dp.start_polling(variables.bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
