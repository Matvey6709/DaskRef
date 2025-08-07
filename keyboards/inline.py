from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.variables import chat_url

builderAdmin = InlineKeyboardBuilder()
builderAdmin.add(
    InlineKeyboardButton(text="Админ панель(ограниченный круг лиц)", callback_data="admin_value", ))

builderAdmin2 = InlineKeyboardBuilder()
builderAdmin2.add(
    InlineKeyboardButton(text="Заявки на вывод средств", callback_data="money_value", ))
builderAdmin2.add(
    InlineKeyboardButton(text="Список всех пользователей", callback_data="users_value", ))
builderAdmin2.add(
    InlineKeyboardButton(text="Статистика", callback_data="static_value", ))
builderAdmin2.adjust(2)

builderAdmin3 = InlineKeyboardBuilder()
builderAdmin3.add(
    InlineKeyboardButton(text="Заявки на вывод средств", callback_data="money_value", ))
builderAdmin3.add(
    InlineKeyboardButton(text="Загрузка", callback_data="random", ))
builderAdmin3.add(
    InlineKeyboardButton(text="Статистика", callback_data="static_value", ))
builderAdmin3.adjust(2)

builderAdmin4 = InlineKeyboardBuilder()
builderAdmin4.add(
    InlineKeyboardButton(text="Загрузка", callback_data="money_value", ))
builderAdmin4.add(
    InlineKeyboardButton(text="Список всех пользователей", callback_data="users_value", ))
builderAdmin4.add(
    InlineKeyboardButton(text="Статистика", callback_data="static_value", ))
builderAdmin4.adjust(2)

pay_value = InlineKeyboardBuilder()
pay_value.add(InlineKeyboardButton(
    text="Выплата",
    callback_data="spam_pay_value")
)

builder_sub = InlineKeyboardBuilder()
for i in chat_url:
    builder_sub.add(InlineKeyboardButton(
        text="Подписаться", url=str(i),
        callback_data="random_value")
    )
builder_sub.add(InlineKeyboardButton(
        text="Проверить",
        callback_data="check_sub")
    )
builder_sub.adjust(1)

builderListUsers = InlineKeyboardBuilder()
builderListUsers.add(
    InlineKeyboardButton(text="⬅️", callback_data="list_users_left_value", ))
builderListUsers.add(
    InlineKeyboardButton(text="➡️", callback_data="list_users_right_value", ))

