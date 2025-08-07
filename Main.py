from aiogram import Bot, Dispatcher, executor, types
import os
from aiogram.dispatcher.filters import Text
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token="7529120639:AAFfxyQxHncEdhBd0PgTNvoiCEN5f85F5Q0")
dp = Dispatcher(bot)

button_z = KeyboardButton('💎 Заработать', callback_data='btn1')
button_k = KeyboardButton('💼 Кабинет', callback_data='btn2')
button_i = KeyboardButton('📋 Информация', callback_data='btn3')
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
greet_kb.row(button_z, button_k)
greet_kb.add(button_i)


@dp.message_handler(commands='start')
async def start(mes):
    await mes.answer('Привет! Я бот, который проверит твою подписку на канал.', reply_markup=greet_kb)
    # await check_subscribe(mes)



@dp.message_handler()
async def check_subscribe(mes):
    chat_id = '-1002134305326'
    user_channel_status = await bot.get_chat_member(chat_id=chat_id,
                                                    user_id=mes.from_user.id)

    if user_channel_status['status'] != 'left':
        await mes.answer('Вы подписанны на канал, можете получать контент!')
        await send_content(mes)
        return True

    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Подписаться',
                                              url='https://t.me/+NV69Akn5BvkwMjcy'))

        await mes.answer('Для получения контента необходимо подписаться на канал!',
                         reply_markup=markup)
        # await mes.answer('После подписки напишите любое сообщение для проверки')
@dp.message_handler(lambda message: message.text == "Заработать")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно!")

@dp.message_handler(Text(equals="💎 Заработать"))
async def with_puree(msg):
    await msg.reply("Отличный выбор!")

# @dp.message_handler(content_types=["text"])
# async def btn_f(mes):
#     print(mes)
#     if mes == '💎 Заработать':
#         print("Заработать")
#     if mes == '💼 Кабинет':
#         print("Кабинет")
#     if mes == '📋 Информация':
#         print("Информация")



@dp.message_handler()
async def send_content(mes):
    await mes.answer('Контент')


if __name__ == '__main__':
    executor.start_polling(dp)
