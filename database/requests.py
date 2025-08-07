import json

from database.models import async_session, Money
from database.models import User, Channel
from sqlalchemy import select
from utils.utils import get_now_time, get_refer_id
from aiogram.filters.command import CommandObject
import pickle

async def set_user(tg_id: int, command: CommandObject) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, ref_id=str(get_refer_id(command.args)), data_reg=get_now_time(), ref='[]',
                             ref_old='[]'))
            await session.commit()


async def get_user(tg_id: int):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))


async def get_users():
    async with async_session() as session:
        return await session.scalars(select(User))


async def count_users():
    async with async_session() as session:
        all_users = await get_users()
        return len(all_users.all())


async def completed_ref(tg_id: int):
    async with async_session() as session:
        user_ref = await get_user(tg_id)
        if user_ref.ref_id != 'None':
            user = await session.scalar(select(User).where(User.tg_id == user_ref.ref_id))
            if user is None:
                return
            if user_ref.tg_id != user.tg_id:
                deserialized1 = json.loads(user.ref)
                bol = False
                for i in deserialized1:
                    if i == user_ref.tg_id:
                        bol = True
                deserialized2 = json.loads(user.ref_old)
                for i in deserialized2:
                    if i == user_ref.tg_id:
                        bol = True
                if not bol:
                    deserialized1.append(user_ref.tg_id)
                    serialized = json.dumps(deserialized1)
                    user.ref = serialized
                    session.add(user)
                await session.commit()


async def count_ref(tg_id: int):
    async with async_session() as session:
        user = await get_user(tg_id)
        deserialized = json.loads(user.ref)
        return len(deserialized)


async def set_user_money(tg_id: int) -> None:
    async with async_session() as session:
        user = await get_user(tg_id)
        session.add(Money(tg_id=tg_id, ref_id=user.ref_id, data_reg=get_now_time(), ref=user.ref, ref_old=user.ref_old))
        await session.commit()


async def reset_user_ref(tg_id: int) -> None:
    async with async_session() as session:
        user = await get_user(tg_id)
        user.ref_old = f'{(json.loads(user.ref_old) + json.loads(user.ref))}'
        user.ref = '[]'
        session.add(user)
        await session.commit()


async def get_money():
    async with async_session() as session:
        return await session.scalars(select(Money))


async def del_user_money(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(Money).where(User.tg_id == tg_id))
        await session.delete(user)
        await session.commit()


async def add_all_money(money1: int) -> None:
    async with async_session() as session:
        try:
            channel = await session.scalar(select(Channel).where(Channel.id == 1))
            print(channel.name)
            channel.name = f'{int(channel.name) + money1}'

            session.add(channel)
        except:
            session.add(Channel(name="0"))
        await session.commit()

async def get_all_money() -> None:
    async with async_session() as session:
        try:
            channel = await session.scalar(select(Channel).where(Channel.id == 1))
            print(channel.name, channel.id)
            return channel.name
        except:
            return "0"


async def get_user_count(count: int) -> None:
    async with async_session() as session:
        count_users1 = await count_users()
        users = await get_users()
        return users.fetchall()[count_users1-1-count]
        # for i in users.all().count():
        #
        # print(users)

