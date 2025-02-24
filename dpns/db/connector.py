from sqlalchemy import select, update, delete, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from dpns.db.db import get_session, use_db
from dpns.libs.token_generator import generate_token, hash_md5
from dpns.db.models.token import Token
from dpns.db.models.user import User
from dpns.db.models.device import Device
from dpns.db.models.device_type import DeviceType
from dpns.db.models.device_admin import DeviceAdmin
from dpns.db.models.problem import Problem
from dpns.db.models.problem_type import ProblemType
from dpns.db.models.problem_author import ProblemAuthor


class Controller():
    """ Users """

    @use_db
    async def create_user(self, session: AsyncSession, login: str | None = None, tg_id: int | None = None, role: str = "user"):
        if login is None and tg_id is None:
            return "User must have tg_id or login"
        user = User(login=login, tg_id=tg_id, role=role)
        session.add(user)
        await session.commit()

    @use_db
    async def get_user(self, session: AsyncSession, user_id: int | None = None, login: str | None = None, tg_id: int | None = None):
        if [user_id, login, tg_id].count(None) != 2:
            return "You should choose one parameter: user_id, login or tg_id"
        if user_id is not None:
            user = (await session.execute(select(User).filter(User.id == user_id))).scalar()
        if login is not None:
            user = (await session.execute(select(User).filter(User.login == login))).scalar()
        if tg_id is not None:
            user = (await session.execute(select(User).filter(User.tg_id == tg_id))).scalar()
        return user

    @use_db
    async def change_role(self, session: AsyncSession, new_role: str, user_id: int | None = None, login: str | None = None, tg_id: int | None = None):
        if [user_id, login, tg_id].count(None) != 2:
            return "You should choose one parameter: user_id, login or tg_id"
        if user_id is not None:
            user = (await session.execute(select(User).filter(User.id == user_id))).scalar()
        if login is not None:
            user = (await session.execute(select(User).filter(User.login == login))).scalar()
        if tg_id is not None:
            user = (await session.execute(select(User).filter(User.tg_id == tg_id))).scalar()
        user.role = new_role
        await session.commit()

    @use_db
    async def delete_user(self, session: AsyncSession, user_id: int | None = None, login: str | None = None, tg_id: int | None = None):
        if [user_id, login, tg_id].count(None) != 2:
            return "You should choose one parameter: user_id, login or tg_id"
        if user_id is not None:
            await session.execute(delete(User).filter(User.id == user_id))
        if login is not None:
            await session.execute(delete(User).filter(User.login == login))
        if tg_id is not None:
            await session.execute(delete(User).filter(User.tg_id == tg_id))
        await session.commit()

    @use_db
    async def connect_tg(self, session: AsyncSession, tg_id: int | None = None, user_id: int | None = None, login: str | None = None):
        if [user_id, login].count(None) != 1:
            return "You should choose one parameter: user_id or login"
        if user_id is not None:
            user = (await session.execute(select(User).filter(User.id == user_id))).scalar()
        if login is not None:
            user = (await session.execute(select(User).filter(User.login == login))).scalar()
        if user.tg_id is not None:
            return "User already connect tg"
        # TODO: add code to change id user old to new
        await session.execute(delete(User).filter(User.tg_id == tg_id))  # delete old tg id user
        user.tg_id = tg_id
        await session.commit()

    @use_db
    async def delete_tg(self, session: AsyncSession, user_id: int | None = None, login: str | None = None):
        if [user_id, login].count(None) != 1:
            return "You should choose one parameter: user_id or login"
        if user_id is not None:
            user = (await session.execute(select(User).filter(User.id == user_id))).scalar()
        if login is not None:
            user = (await session.execute(select(User).filter(User.login == login))).scalar()
        if user.tg_id is None:
            return "User didn't connected tg"
        user.tg_id = None
        await session.commit()

    """ Tokens """

    @use_db
    async def add_token(self, session: AsyncSession, name: str, role: str):
        if (await session.execute(select(Token).filter(Token.name == name))).scalar() is not None:
            return "Token with this name already exist"
        token_text = generate_token()
        token_hash = hash_md5(token_text)
        token = Token(name=name, token=token_hash, role=role)
        session.add(token)
        await session.commit()
        return token_text

    @use_db
    async def del_token(self, session: AsyncSession, name):
        if (await session.execute(select(Token).filter(Token.name == name))).scalar() is None:
            return "Token with this name don't exist"
        await session.execute(delete(Token).filter(Token.name == name))
        await session.commit()
        return "Token deleted"

    @use_db
    async def check_token(self, session: AsyncSession, token_text: str):
        res = (await session.execute(select(Token).filter(Token.token == hash_md5(token_text)))).scalar()
        await session.commit()

        if res is not None:
            return res.role
        return False


controller = Controller()

# test
import asyncio
# asyncio.run(controller.create_user(login="lol888"))
# asyncio.run(controller.change_role(login="lol888", new_role="admin"))
# asyncio.run(controller.delete_user(login="lol888"))
# asyncio.run(controller.connect_tg(login="lol647", tg_id=12312312312))
# asyncio.run(controller.delete_tg(login="lol647"))
# print(asyncio.run(controller.add_token("lol", "admin")))
# print(asyncio.run(controller.check_token("4c10953948de466caaac1b98619ec8b1")))
# print(asyncio.run(controller.del_token("lol")))
