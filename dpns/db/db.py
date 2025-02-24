from asyncio import current_task
from typing import Any, AsyncGenerator, cast, Callable
from functools import wraps
from sqlalchemy import NullPool
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session
from dpns.config import settings


DB = (f"{settings.db_driver}://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:"
      f"{settings.postgres_port}/{settings.postgres_db}")
engine = create_async_engine(DB, echo=False, poolclass=NullPool)
Base = declarative_base()
_async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore[call-overload]
_async_session = async_scoped_session(_async_session_factory, current_task)


async def get_session() -> AsyncGenerator[AsyncSession, AsyncSession]:
    """Function for getting AsyncSession"""
    async with _async_session() as session:
        yield cast(AsyncSession, session)


def use_db(func: Callable[..., Any]) -> Callable[..., Any]:  # type: ignore[misc]
    """Use db session

    Insert session object into your function.

    example:

    @user_db
    async def get_user(session)
        ...

    where session is require param, get session's object


    Args:
        - func (Callable[..., Any]) -

    Return:
        Callable[..., Any] - [description]
    """

    @wraps(func)
    async def wrapper(self: Any, *args: Any, **kwarg: Any) -> Any:  # type: ignore[misc]
        async with _async_session() as session:
            session = cast(AsyncSession, session)
            res = await func(self, session, *args, **kwarg)
            await session.close()
            return res

    return wrapper
