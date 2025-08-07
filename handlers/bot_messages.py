import re

from aiogram import F, Router
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

import utils.variables
from utils import variables
from utils.variables import bot, curs, chat_id
from database.requests import completed_ref, count_ref, count_users, get_all_money
from keyboards.inline import pay_value, builder_sub

router = Router()


@router.message(F.text == "💎 Заработать")
async def with_puree(message: Message):
    # UsrInfo = await bot.get_chat_member(7207136417, 7207136417)
    # print(UsrInfo)
    await check_subscribe(message)


@router.message(F.text == "💼 Кабинет")
async def with_puree(message: Message):
    await check_subscribe(message)


@router.message(F.text == "📋 Информация")
async def with_puree(message: Message):
    await check_subscribe(message)


@router.message()
async def check_subscribe(message):

    check_b = False
    for i in range(len(chat_id)):
        user_channel_status = await bot.get_chat_member(chat_id=chat_id[i],
                                                        user_id=message.from_user.id)
        matches = re.findall(r"'(.+?)'", str(user_channel_status))
        if matches[0] == 'left':
            check_b = True
    if not check_b:
        await completed_ref(message.from_user.id)
        if message.text == "💎 Заработать":
            await message.reply(
                f"👥 Приглашайте друзей и зарабатывайте, за каждого друга, который выполнит условия, получите {curs} ₽\n"
                f'🚀 Вот твоя персональная ссылка на приглашение: \n'
                f'<code>https://t.me/daskref_bot?start={message.from_user.id}</code>'
                , parse_mode='HTML')
        if message.text == "💼 Кабинет":
            us = await count_ref(message.from_user.id)
            async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
                # user_info = await get_user_data(user_id=message.from_user.id)
                text = (f'👉 Ваш телеграм ID: <b>{message.from_user.id}</b>\n'
                        f'👥 Количество приглашенных тобой пользователей, которые выполнили условия: <b>{us}</b>\n'
                        f'💵 Заработано: {us*curs} ₽ (курс: 1 реферал = {curs} ₽)\n'
                        f'Вывести можно от {variables.count_ref * curs} ₽')

            await message.answer(text, parse_mode='HTML', reply_markup=pay_value.as_markup())
        if message.text == "📋 Информация":
            count_users_ = await count_users()
            await message.reply(f"Всего пользователей: {count_users_}\n"
                                f"Выплачено всего: {await get_all_money()}")
    else:

        await message.answer(
            'Чтобы продолжить необходимо подписаться на канал(ы)!\n(для проверки опять нажми на кнопку)',
            reply_markup=builder_sub.as_markup(resize_keyboard=True))

