import json
import re

from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.variables import chat_id
import utils.variables
from database import requests
from handlers.bot_messages import check_subscribe
from utils.variables import bot, count_ref, curs
from database.requests import get_users, get_user, set_user_money, reset_user_ref, get_money, set_test2, del_user_money, \
    add_all_money, get_user_count, count_users
from keyboards.inline import builderAdmin2, builderAdmin3, pay_value, builderAdmin4, builderListUsers
from utils.utils import get_username_by_id, info_user
from typing import Any
from time import monotonic

from aiogram import Router, F

from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage

router = Router()


@router.callback_query(F.data == "admin_value")
async def send_random_value(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=builderAdmin2.as_markup())


@router.callback_query(F.data == "money_value")
async def send_random_value(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=builderAdmin4.as_markup())
    try:
        users = await get_money()
        r = 0
        if users is not None:
            for i in users:
                refs = ""
                refs1 = (json.loads(i.ref))
                for j in refs1:
                    refs += f'@{await get_username_by_id(bot, int(j))} '
                text1 = (f'Номер: {i.id}\n'
                         f'Имя пользователя: @{await get_username_by_id(bot, i.tg_id)}\n'
                         f'Кого пригласил пользователь: ({len(refs1)}){refs}\n'
                         f'Кто пригласил пользователя: @{await get_username_by_id(bot, i.ref_id)}\n'
                         f'Дата регистрации: {i.data_reg}\n'
                         f'Заработал: {len(refs1) * curs} ₽\n')
                builderWard = InlineKeyboardBuilder()
                builderWard.add(
                    InlineKeyboardButton(text="Выплатил", callback_data=f"ward{r}_value", ))

                @router.callback_query(F.data == f"ward{r}_value")
                async def send_random_value(callback: CallbackQuery):
                    await del_user_money(i.tg_id)
                    await callback.message.delete()
                    await add_all_money(int(len(refs1) * curs))

                r += 1
                await callback.message.answer(text1, reply_markup=builderWard.as_markup())
    except:
        await callback.message.answer("Нету людей")

    await callback.message.edit_reply_markup(reply_markup=builderAdmin2.as_markup())


@router.callback_query(F.data == "users_value")
async def send_random_value(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=builderAdmin3.as_markup())


    i = await get_user_count(0)
    text1 = await info_user(i)

    await callback.message.answer(text1, reply_markup=builderListUsers.as_markup())

    await callback.message.edit_reply_markup(reply_markup=builderAdmin2.as_markup())


@router.callback_query(F.data == "static_value")
async def send_random_value(callback: CallbackQuery):
    await set_test2(callback.from_user.id)


@router.callback_query(F.data == "spam_pay_value")
async def send_random_value(callback: CallbackQuery):
    tg_id = str(callback.from_user.id)
    user = await get_user(tg_id)
    if len(json.loads(user.ref)) >= count_ref:
        await set_user_money(tg_id)
        await reset_user_ref(tg_id)
        us = await requests.count_ref(callback.from_user.id)
        text = (f'👉 Ваш телеграм ID: <b>{callback.from_user.id}</b>\n'
                f'👥 Количество приглашенных тобой пользователей, которые выполнили условие: <b>{us}</b>\n'
                f'💵 Заработано: {us * curs} ₽ (курс: 1 реферал = {curs} ₽)\n'
                f'Вывести можно от {count_ref * curs} ₽')
        await callback.message.edit_text(text, parse_mode='HTML', reply_markup=pay_value.as_markup())
        await callback.message.answer("Ваша заявка на вывод средств добавлена")
    else:
        await callback.answer("Не достаточно приглашённых людей для вывода средств", show_alert=True)


@router.callback_query(F.data.startswith("spam"))
async def callback_query_handler(callback_query: CallbackQuery, storage: MemoryStorage) -> Any:
    user_id = str(callback_query.from_user.id)

    user_storage = await storage.get_data(user_id)

    if int(callback_query.data[4:]) == user_storage["data"][2]:
        time = monotonic()
        await callback_query.message.answer("<PLACEHOLDER>")
        user_storage["data"] = [time, False, 0]
        await storage.set_data(user_id, user_storage)
        await callback_query.message.delete()


@router.callback_query(F.data == "list_users_left_value" or F.data == "list_users_right_value")
async def send_random_value(callback: CallbackQuery):
    # action = callback_data.get('action')
    # floor = callback_data.get('floor')
    # floor += int(action)
    # if floor < 0:
    #     floor = 0
    # c = await count_users()
    # if floor >= c:
    #     floor = c-1
    # i = await get_user_count(floor)
    # text1 = await info_user(i)
    builderListUsers1 = InlineKeyboardBuilder()
    builderListUsers1.add(
        InlineKeyboardButton(text="⬅️", callback_data="list_users_left_value"))
    builderListUsers1.add(
        InlineKeyboardButton(text="➡️", callback_data="list_users_right_value"))

    await callback.message.edit_text(f"text1", reply_markup=builderListUsers1.as_markup())


@router.callback_query(F.data == "list_users_right_value")
async def send_random_value(callback: CallbackQuery):

    await callback.message.edit_text("right", reply_markup=builderListUsers.as_markup())

@router.callback_query(F.data == "check_sub")
async def send_random_value(callback: CallbackQuery):
    check_b = False
    for i in range(len(chat_id)):
        user_channel_status = await bot.get_chat_member(chat_id=chat_id[i],
                                                        user_id=callback.from_user.id)
        matches = re.findall(r"'(.+?)'", str(user_channel_status))
        if matches[0] == 'left':
            check_b = True
    if not check_b:
        await callback.answer("Вы подписаны не на все каналы", show_alert=True)
    else:
        await callback.answer("Молодец! Теперь можешь продолжить пользоваться ботом", show_alert=True)
        await callback.message.edit_text(f"Можешь продолжить пользоваться ботом")