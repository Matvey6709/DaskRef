import json
from datetime import datetime
import pytz

from utils.variables import curs, bot


def get_now_time():
    now = datetime.now(pytz.timezone('Europe/Moscow'))
    # Convert to naive datetime
    return str(now.replace(tzinfo=None))


# достаем refer_id из команды /start
def get_refer_id(command_args):
    try:
        return int(command_args)
    except (TypeError, ValueError):
        return None


async def get_username_by_id(bot, id):
    try:
        user = await bot.get_chat(id)
        return user.username
    except:
        return None

async def info_user(i):
    text1 = ""
    refs = ""
    refs1 = (json.loads(i.ref))
    for j in refs1:
        refs += f'@{await get_username_by_id(bot, int(j))} '
    text1 += (f'Номер: {i.id}\n'
              f'Имя пользователя: @{await get_username_by_id(bot, i.tg_id)}\n'
              f'Кого пригласил пользователь: ({len(refs1)}){refs}\n'
              f'Кто пригласил пользователя: @{await get_username_by_id(bot, i.ref_id)}\n'
              f'Дата регистрации: {i.data_reg}\n'
              f'Заработал: {len(refs1) * curs} ₽\n'
              f'------------------------------------------\n')
    return text1