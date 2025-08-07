from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)




class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    ref_id: Mapped[str] = mapped_column()
    ref_old: Mapped[str] = mapped_column()
    ref: Mapped[str] = mapped_column()
    data_reg: Mapped[str] = mapped_column(String(20))


class Money(Base):
    __tablename__ = 'money'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    ref_id: Mapped[str] = mapped_column()
    ref: Mapped[str] = mapped_column()
    ref_old: Mapped[str] = mapped_column()
    data_reg: Mapped[str] = mapped_column(String(20))


class Channel(Base):
    __tablename__ = 'channel'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
